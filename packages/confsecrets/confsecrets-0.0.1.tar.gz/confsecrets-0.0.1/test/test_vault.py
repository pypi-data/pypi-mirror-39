from unittest import TestCase
import tempfile
import json
import os

from confsecrets.vault import *
from confsecrets.pbe import InvalidMessageAuthenticationCode


RAW_DATA = {
    'magic': VAULT_MAGIC,
    'data': {
        'abc': '9utDFQuNAFgi88JMMdnhRjV6ChBlEBHVuyTJb1ImDr7VH9Q3FM4nIhP80hL12uuVy+1y',
        'def': 'CHDdVTfbAPu6Z47cb4bSfe9LXq0yZLfJm2M2w+FgHwnO9xkYH/ry9v9olCePLuWaUN5R',
    }
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestExistingVault(TestCase):

    def setUp(self):
        self.salt = b'\xe2\x98\xe5\xdc\xeb\xf5\xcc\xd8'
        self.password = 'This is just a test'

        fd, fnm = tempfile.mkstemp(prefix='vault-')
        os.write(fd, json.dumps(RAW_DATA).encode('utf-8'))
        os.write(fd, b'\n')
        os.close(fd)
        self.path = fnm
        self.vault = Vault(self.salt, self.password, self.path)

    def tearDown(self):
        if os.path.exists(self.path):
            os.unlink(self.path)

    def test_vault_keys(self):
        actual_keys = sorted(self.vault.keys())
        self.assertEqual(actual_keys, ['abc', 'def'])

    def test_vault_len(self):
        self.assertEqual(len(self.vault), 2)

    def test_vault_items(self):
        actual_items = sorted(self.vault.items(), key=lambda item: item[0])
        self.assertEqual(actual_items, [('abc', 'xyz'), ('def', 'fed')])

    def test_vault_getitem(self):
        encrypted_value = self.vault.data['abc']
        self.assertEqual(encrypted_value, '9utDFQuNAFgi88JMMdnhRjV6ChBlEBHVuyTJb1ImDr7VH9Q3FM4nIhP80hL12uuVy+1y')
        decrypted_value = self.vault['abc']
        self.assertEqual(decrypted_value, 'xyz')

    def test_vault_in(self):
        self.assertIn('abc', self.vault)

    def test_vault_setitem(self):
        self.assertNotIn('PASSWORD', self.vault)
        expected_value = 'Every g;;d boy does f1ne'
        self.vault['PASSWORD'] = expected_value
        self.assertIn('PASSWORD', self.vault)

        othervault = Vault(self.salt, self.password, self.path)
        actual_value = othervault['PASSWORD']
        self.assertEqual(actual_value, expected_value)

    def test_bad_salt(self):
        bad_salt = os.urandom(8)
        othervault = Vault(bad_salt, self.password, self.path)

        with self.assertRaises(InvalidMessageAuthenticationCode):
            othervault['abc'] == 'xyz'

    def test_bad_password(self):
        bad_password = 'This is the wrong password'
        othervault = Vault(self.salt, bad_password, self.path)

        with self.assertRaises(InvalidMessageAuthenticationCode):
            othervault['abc'] == 'xyz'


class TestNewVault(TestCase):

    def setUp(self):
        self.salt = b'\xe2\x98\xe5\xdc\xeb\xf5\xcc\xd8'
        self.password = 'This is just a test'

        fd, fnm = tempfile.mkstemp(prefix='vault-')
        os.close(fd)
        os.unlink(fnm)
        self.path = fnm
        self.vault = Vault(self.salt, self.password, self.path)

    def tearDown(self):
        if os.path.exists(self.path):
            os.unlink(self.path)

    def test_vault_len(self):
        self.assertEqual(len(self.vault), 0)

    def test_vault_setitem(self):
        self.assertNotIn('PASSWORD', self.vault)
        expected_value = 'Every g;;d boy does f1ne'
        self.vault['PASSWORD'] = expected_value
        self.assertIn('PASSWORD', self.vault)

        othervault = Vault(self.salt, self.password, self.path)
        actual_value = othervault['PASSWORD']
        self.assertEqual(actual_value, expected_value)
