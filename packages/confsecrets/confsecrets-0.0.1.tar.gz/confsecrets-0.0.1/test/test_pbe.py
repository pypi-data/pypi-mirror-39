from unittest import TestCase
from base64 import b64decode, b64encode

from confsecrets.pbe import *


class TestPBEUtil(TestCase):

    def setUp(self):
        self.salt = b'\xe2\x98\xe5\xdc\xeb\xf5\xcc\xd8'

    def test_encrypt_decrypt(self):
        """
        Verify that the cryptor can do a roound trip encryption
        """
        expected_text = 'This message must go round a bunch'
        pbe = PBEUtil('This is the password', self.salt)
        crypt_message = pbe.encrypt(expected_text)
        actual_text = pbe.decrypt(crypt_message)
        self.assertEqual(actual_text, expected_text)

    def test_key_derivation(self):
        """
        Test that key derived from the same password is the same
        """
        pbe = PBEUtil('This is the password', self.salt)
        other_pbe = PBEUtil('This is the password', self.salt)
        self.assertEqual(pbe.key, other_pbe.key)

    def test_diff_password_diff_key(self):
        """
        Test that changes the password changes the key
        """
        pbe = PBEUtil('This is the password', self.salt)
        other_pbe = PBEUtil('This is the other password', self.salt)
        self.assertNotEqual(pbe.key, other_pbe.key)

    def test_diff_salt_diff_key(self):
        """
        Test that changing the salt changes the key
        """
        pbe = PBEUtil('This is the password', self.salt)
        other_pbe = PBEUtil('This is the password', salt=b'\x88\xb0m*\x92\x18\xab\xc3')
        self.assertNotEqual(pbe.key, other_pbe.key)

    def test_length_error(self):
        """
        Test that the length of the message is checked
        """
        pbe = PBEUtil('This is the password', self.salt)
        message = pbe.encrypt('This is the message')
        message_bytes = b64decode(message)
        truncated_message = b64encode(message_bytes[0:47])
        with self.assertRaises(MessageTooShort):
            pbe.decrypt(truncated_message)

    def test_mac_error(self):
        """
        Test that the MAC is checked
        """
        pbe = PBEUtil('This is the password', self.salt)
        message = pbe.encrypt('This is the message')
        message_bytes = bytearray(b64decode(message))
        # We use XOR here because we need to know it will change
        message_bytes[20] = message_bytes[20] ^ 0xff
        altered_message = b64encode(message_bytes)
        with self.assertRaises(InvalidMessageAuthenticationCode):
            pbe.decrypt(altered_message)


class TestPasswordUtil(TestCase):

    def test_too_short(self):
        """
        PasswordTooSimple exception should be raised if the password is too short.
        """
        with self.assertRaises(PasswordTooSimple):
            PasswordUtil.check('abc')

    def test_too_simple(self):
        """
        PasswordTooSimple exception should be raised if the password does not have 
        the required character classes.
        """
        with self.assertRaises(PasswordTooSimple):
            PasswordUtil.check('11abcdefghijKLMNOPqrstuv22')

    def test_not_shell_safe(self):
        """
        PasswordNotShellSafe exception should be raised if the password requires 
        escaping from a Linux shell
        """
        with self.assertRaises(PasswordNotShellSafe):
            PasswordUtil.check('11abcdefghijKL   -MNOPqrstuv22')
        with self.assertRaises(PasswordNotShellSafe):
            PasswordUtil.check('11abcdefghijKL${HOME}MNOPqrstuv22')

    def test_ok(self):
        """
        No exception is raised for a vaild password
        """
        PasswordUtil.check('11,abcdefghijKLMNOPqrstuv,22')

    def test_generate(self):
        """
        Password is generated of the appropriate length
        """
        length = len(PasswordUtil.generate(length=2))
        self.assertEqual(length, PasswordUtil.min_length)
        extra_length = len(PasswordUtil.generate(length=16))
        self.assertEqual(extra_length, 16)
