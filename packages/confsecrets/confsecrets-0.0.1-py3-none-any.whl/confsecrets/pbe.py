"""
Wrap PyCrypto for safe and effective Password Based Encryption (PBE)
"""
from base64 import b64encode, b64decode
import string
from enum import Enum
from six.moves import shlex_quote

from Crypto import Random
from Crypto.Random import random
from Crypto.Hash.HMAC import HMAC
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

__all__ = [
    'InvalidSalt',
    'MessageTooShort',
    'InvalidMessageAuthenticationCode',
    'PasswordTooSimple',
    'PasswordNotShellSafe',
    'PasswordUtil',
    'PBEUtil',
    'CClass',
]


class InvalidSalt(Exception):
    """
    The salt must be an 8-byte bytes object
    """
    pass


class MessageTooShort(Exception):
    """
    Encrypted message/password too short; the encrypted message must be at least 48 bytes.
    """
    pass


class InvalidMessageAuthenticationCode(Exception):
    """
    Message authentication code invalid; the encrypted message must have been created
    by different software or with a different password.
    """
    pass


class PasswordTooSimple(Exception):
    """
    The password must be at least 12 characters long and include an uppercase letter,
    a lower case letter, a symbol, and a digit.
    """
    pass


class PasswordNotShellSafe(Exception):
    """
    This password requires quoting in a bash shell, and thus causes operational risk.
    """
    pass


class CClass(Enum):
    """
    Enumeration of ascii character classes that knows how to characterize strings
    and generate sub-strings for each character class
    """
    LOWER = 1
    UPPER = 2
    DIGIT = 3
    SYMBOL = 4
    SPACE = 5
    OTHER = 6

    @classmethod
    def classes(cls, password):
        """
        Returns the set of character classes contained in the input
        """
        def character2class(char):
            if char in string.ascii_lowercase:
                return cls.LOWER
            elif char in string.ascii_uppercase:
                return cls.UPPER
            elif char in string.digits:
                return cls.DIGIT
            elif char in string.punctuation:
                return cls.SYMBOL
            elif char in string.whitespace:
                return cls.SPACE
            return cls.OTHER
        return set(map(character2class, password))

    def characters(self):
        """
        Returns the characters in the given character class, except for CClass.OTHER
        """
        if self == CClass.LOWER:
            return string.ascii_lowercase
        elif self == CClass.UPPER:
            return string.ascii_uppercase
        elif self == CClass.DIGIT:
            return string.digits
        elif self == CClass.SYMBOL:
            return ''.join(filter(lambda c: shlex_quote(c) == c, string.punctuation))
        elif self == CClass.SPACE:
            return self.whitespace
        return None


class PasswordUtil():
    """
    Utility class for checking password complexity and generating passwords.
    """
    required_classes = {CClass.LOWER, CClass.UPPER, CClass.DIGIT, CClass.SYMBOL}
    min_length = 12

    @classmethod
    def check(cls, password):
        """
        Checks password strength as follows:
            - At least min_length characters
            - At least one lowercase, uppercase, numeric, and symbolic character
            - Safe for the Linux shell, e.g. does not require escaping

        :param password: a password string
        :return: nothing if password is OK, raises if password is not ok
        """
        # Check password length
        if len(password) < cls.min_length:
            raise PasswordTooSimple
        # Map characters to character classes
        classes = CClass.classes(password)
        # Make sure you have needed classes
        if not cls.required_classes.issubset(classes):
            raise PasswordTooSimple()
        # Check if the password is safe for the shell
        if shlex_quote(password) != password:
            raise PasswordNotShellSafe()

    @classmethod
    def generate(cls, length=0):
        """
        Generate a new password
        :param length: a length for the password
        :return: a password that meets requirements above
        """
        if length < cls.min_length:
            length = cls.min_length
        required_classes = list(cls.required_classes)

        def generate_candidate(length):
            bpass = bytearray(length)
            for i in range(length):
                cclass = random.choice(required_classes)
                bpass[i] = ord(random.choice(cclass.characters()))
            return bpass.decode('ascii')
        # each candidate is very likely to meet the requirements, but let's be sure
        while True:
            candidate = generate_candidate(length)
            try:
                cls.check(candidate)
                return candidate
            except PasswordTooSimple:
                pass


class PBEUtil(object):
    """
    A Cryptor handles symmetric encryption using binary keys derived from clear text keys
    The algorithm for key derivation is PBKDF2 with SHA256.
    The algorithm for encryption is AES 256 (key_size==32 bytes).
    By default there are 1007 iterations.
    The message includes the IV and the encrypted data.
    There is no message authentication on these, the HMAC is used only in key derivation.

    See RFC-2898 for a definition of the algorithms.
    """
    iterations = 1007
    key_size = 32

    def __init__(self, password, salt):
        if not isinstance(password, bytes):
            password = str(password).encode('utf-8')
        try:
            salt = bytes(salt)
            assert len(salt) == 8
        except Exception:
            raise InvalidSalt
        self.password = password
        if salt is not None:
            self.salt = bytes(salt)
        self.__key = None

    @property
    def key(self):
        """
        Compute a derived key based on attributes on this object.
        """
        if self.__key is None:
            def proof(password, salt):
                return HMAC(password, salt, SHA256).digest()
            self.__key = PBKDF2(self.password, self.salt, self.key_size, self.iterations, prf=proof)
        return self.__key

    def encrypt_guts(self, cleartext):
        """
        Encrypt some clear text and return and encrypted message bytes

        :param cleartext: a str
        :return: encrypted message including the IV and the ciphertext
        """
        if isinstance(cleartext, str):
            cleartext = cleartext.encode('utf-8')
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CFB, iv)
        ciphertext = cipher.encrypt(cleartext)
        return iv + ciphertext

    def decrypt_guts(self, message):
        """
        Decrypt a message using an IV and some encrypted bytes

        :param: message: must be bytes including iv and ciphertext
        :return: A clear text string
        """
        iv = message[0:16]
        ciphertext = message[16:]
        cipher = AES.new(self.key, AES.MODE_CFB, iv)
        return cipher.decrypt(ciphertext)

    def encrypt(self, cleartext):
        """
        Encrypt some clear text, returning a Base64 message including mac, an iv, and ciphertext

        :param cleartext: a str
        :return: Base64 encoded encrypted bytes with a mac
        """
        message_bytes = self.encrypt_guts(cleartext)
        mac = HMAC(self.key, message_bytes, SHA256).digest()
        return b64encode(mac + message_bytes)

    def decrypt_bytes(self, message):
        """
        Decrypt a message that is encoded in Base64 consisting of a mac, an iv, and ciphertext

        :param: message: must be a base64 encoded string
        :return: A clear byte string
        """
        message_bytes = b64decode(message)
        if len(message_bytes) < 48:
            raise MessageTooShort()
        expect_mac = message_bytes[0:32]
        actual_mac = HMAC(self.key, message_bytes[32:], SHA256).digest()
        if actual_mac != expect_mac:
            raise InvalidMessageAuthenticationCode()
        return self.decrypt_guts(message_bytes[32:])

    def decrypt(self, message):
        """
        Decrypt a message that is encoded in Base64 consisting of a mac, an iv, and ciphertext

        :param: message: must be a base64 encoded string
        :return: A clear text string
        """
        clear_bytes = self.decrypt_bytes(message)
        return clear_bytes.decode('utf-8')
