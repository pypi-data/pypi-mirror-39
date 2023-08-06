import logging

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP


class CryptFile(object):
    """ Encrypt and decrypt file
    """

    def __init__(self, logger=None):
        if (logger):
            self.logger = logger
        else:
            self.logger = logging.getLogger()
            handler = logging.StreamHandler()
            self.logger.addHandler(handler)

    def generate_key(self,
                     private_key_fname='private_key.pem',
                     public_key_fname='public_key.pem',
                     _passphrase=None):
        
        self.logger.debug(
            'generate_key private_key: {}, public_key_fname: {}, pwd = {}'.
            format(private_key_fname, public_key_fname, _passphrase))

        key = RSA.generate(2048)
        private_key = key.export_key(passphrase=_passphrase)

        file_out = open(private_key_fname, 'wb')
        file_out.write(private_key)
        file_out.close()


        public_key = key.publickey().export_key()
        file_out = open(public_key_fname, 'wb')
        file_out.write(public_key)
        file_out.close()
        
    def encrypt_file(self, data_fname, enc_fname=None, public_key_fname='public_key.pem'):
        retVal = None
        self.logger.debug('encrypt_file {} to {} using {}'.format(data_fname, enc_fname, public_key_fname))

        with open(data_fname, 'rb') as data_file:
            data = data_file.read()
            if (not enc_fname):
                enc_fname = '{}.{}'.format(data_fname, 'encrypted')
            self.logger.debug('encrypt_file {} to {} using {}'.format(data_fname, enc_fname, public_key_fname))
            retVal = self.encrypt_data(data, enc_fname, public_key_fname)
        return retVal
    
    def encrypt_data(self, data, enc_fname, public_key_fname='public_key.pem'):
        with open(enc_fname, 'wb') as out_file:
            fKey = open(public_key_fname, 'rb')
            recipient_key = RSA.import_key(fKey.read())
            fKey.close()
            session_key = get_random_bytes(16)

            cipher_rsa = PKCS1_OAEP.new(recipient_key)
            enc_session_key = cipher_rsa.encrypt(session_key)

            cipher_aes = AES.new(session_key, AES.MODE_EAX)
            ciphertext, tag = cipher_aes.encrypt_and_digest(data)
            [
                out_file.write(x)
                for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext)
            ]

    def decrypt_file(self, enc_fname, dec_fname, private_key_fname='private_key.pem', _passphrase=None):
        data = self.decrypt_data(enc_fname, private_key_fname, _passphrase)
        with open(dec_fname, 'wb') as fobj:
            fobj.write(data)
    
    def decrypt_data(self, enc_fname, private_key_fname='private_key.pem', _passphrase=None):
        with open(enc_fname, 'rb') as fobj:
            fKey = open(private_key_fname, 'rb')
            private_key = RSA.import_key(fKey.read(), passphrase=_passphrase)
            fKey.close()
            enc_session_key, nonce, tag, ciphertext = [
                fobj.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1)
            ]

            cipher_rsa = PKCS1_OAEP.new(private_key)
            session_key = cipher_rsa.decrypt(enc_session_key)

            cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
            data = cipher_aes.decrypt_and_verify(ciphertext, tag)
            return data


if __name__ == "__main__":
    crypt_file = CryptFile()
    crypt_file.generate_key()
