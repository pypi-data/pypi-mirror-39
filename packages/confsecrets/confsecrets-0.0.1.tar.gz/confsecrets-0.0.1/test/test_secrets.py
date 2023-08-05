from unittest import TestCase
import tempfile
import os

from confsecrets.vault import Vault, DefaultVault
from confsecrets.secrets import Secret


class TestSecrets(TestCase):
    """
    Test that secrets work

    Because of the init-once and singleton nature of DefaultVault,
    we implement tests for DefaultVault here too.
    """
    def setUp(self):
        self.salt = b'\xe2\x98\xe5\xdc\xeb\xf5\xcc\xd8'
        self.password = 'This is just a test'

        fd, fnm = tempfile.mkstemp(prefix='vault-')
        os.close(fd)
        os.unlink(fnm)
        self.path = fnm
        DefaultVault.init(self.salt, self.password, self.path)
        self.vault = Vault(self.salt, self.password, self.path)

    def tearDown(self):
        if os.path.exists(self.path):
            os.unlink(self.path)

    def test_default_vault_is_singleton(self):
        vault1 = DefaultVault()
        vault2 = DefaultVault()
        self.assertIs(vault1, vault2)

    def test_secret_takes_default_vault(self):
        secret = Secret('PASSWORD')
        self.assertIs(secret.vault, DefaultVault())

    def test_no_secret_means_error(self):
        with self.assertRaises(KeyError):
            secret = Secret('PASSWORD')
            secret.get()

    def test_can_set_secret_value(self):
        one_secret = Secret('API_KEY')
        expected_value = 'cgorcgug1298982498'
        one_secret.set(expected_value)
        secret_with_same_name = Secret('API_KEY')
        actual_value = secret_with_same_name.get()
        self.assertEqual(actual_value, expected_value)

    def test_secret_with_different_vault(self):
        secret = Secret('API_KEY', vault=self.vault)
        self.assertIsNot(secret.vault, DefaultVault())

    def test_secret_acts_like_string(self):
        secret = Secret('API_KEY')
        expected_value = 'cgorcgug1298982498'
        secret.set(expected_value)

        interpolate_it = '%s' % secret
        self.assertEqual(interpolate_it, expected_value)

        cast_it = str(secret)
        self.assertEqual(cast_it, expected_value)

        self.assertTrue(secret.startswith(expected_value))
        self.assertTrue(secret.endswith(expected_value))
