import unittest

from crypt_file import CryptFile


class Test_CryptFile(unittest.TestCase):
    def setUp(self):
        self.crypt_file = CryptFile()
        self._test_secret = 'this is my little secret'

    @unittest.skip("just temporary")
    def test_generate_key(self):
        self.crypt_file.generate_key()
        self.crypt_file.generate_key(
            private_key_fname='private_test.pem',
            public_key_fname='public_test.pem')

        self.crypt_file.generate_key(
            private_key_fname='private_test_pwd.pem',
            public_key_fname='public_test_pwd.pem',
            _passphrase='TestingPassphraseGoesHere')

    def test_encrypt_file(self):
        self.crypt_file.encrypt_file('little_secret.txt')
        self.crypt_file.encrypt_file('little_secret_null')
        self.crypt_file.encrypt_file('little_secret.txt',
                                     'encrypted_secret_default.enc')
        self.crypt_file.encrypt_file(
            'little_secret.txt',
            'encrypted_secret_test.enc',
            public_key_fname='public_test.pem')
        self.crypt_file.encrypt_file(
            'little_secret.txt',
            'encrypted_secret_test_pwd.enc',
            public_key_fname='public_test_pwd.pem')

    def test_encrypt_data(self):
        self.crypt_file.encrypt_data(
            self._test_secret.encode('utf-8'), 'data.encrypted')

    def test_decrypt_file(self):
        self.crypt_file.decrypt_file(
            'encrypted_secret_test.enc',
            'little_secret.txt.dec',
            private_key_fname='private_test.pem')
        with (self.assertRaises(ValueError)):
            self.crypt_file.decrypt_file(
                'encrypted_secret_test_pwd.enc',
                'little_secret_pwd.txt.dec',
                private_key_fname='private_test_pwd.pem')
        self.crypt_file.decrypt_file(
            'encrypted_secret_test_pwd.enc',
            'little_secret_pwd.txt.dec',
            private_key_fname='private_test_pwd.pem',
            _passphrase='TestingPassphraseGoesHere')

    def test_decrypt_data(self):
        data = self.crypt_file.decrypt_data('data.encrypted')
        self.assertEqual(data, self._test_secret.encode('utf-8'))

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
