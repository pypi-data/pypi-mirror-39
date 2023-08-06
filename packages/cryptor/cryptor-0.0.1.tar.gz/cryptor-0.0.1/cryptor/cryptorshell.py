import argparse
import logging

from crypt_file import CryptFile

class CrypterShell(object):

    PGM_VERSION = '0.1'

    def __init__(self):
        self.logger = logging.getLogger()
        handler = logging.StreamHandler()
        self.logger.addHandler(handler)

    def parse_args(self):
        retVal = True

        # construct the argument parse and parse the arguments
        ap = argparse.ArgumentParser(description='Encrypt or decrypt file')
        ap.add_argument(
            "command",
            choices=['encrypt', 'decrypt', 'generate'],
            help="command (encrypt, decrypt, generate) Default: encrypt",
            default='encrypt')
        ap.add_argument('inputfile', help='input file', nargs='?', default=None)
        ap.add_argument('outputfile', help='output file', nargs='?', default=None)
        ap.add_argument(
            "-v",
            "--verbosity",
            help="level of verbosity (DEBUG, INFO, WARNING, ERROR, CRITICAL) Default: DEBUG",
            default='DEBUG')

        ap.add_argument(
            "--privkey",
            help="Private Key (full filename) Default: private_key.pem",
            default='private_key.pem')
    
        ap.add_argument(
            "--pubkey",
            help="Public Key (full filename) Default: public_key.pem",
            default='public_key.pem')

        ap.add_argument(
            "--pwd",
            help="Password for private key",
            default=None)

        args = ap.parse_args()
    
        verb_choices = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        verbose_lvl = 'DEBUG'
        self.logger.setLevel(verbose_lvl)

        if (args.verbosity):
            verbose_lvl = args.verbosity.upper()
            if (verbose_lvl in verb_choices):
                self.logger.setLevel(verbose_lvl)
                self.logger.debug('Verbosity level :{}'.format(verbose_lvl))
            else:
                print('Verbosity must be one of the following values: DEBUG, INFO, WARNING, ERROR, CRITICAL')
                retVal = False

        self._command = args.command
        self.logger.debug('command: {}'.format(self._command))
        
        self._inputfile = args.inputfile
        if (args.inputfile):
            self.logger.debug('input file: {}'.format(self._inputfile))
        else:
            self.logger.debug('input file not set')

        self._outputfile = args.outputfile
        if (args.outputfile):
            self._outputfile = args.outputfile
            self.logger.debug('output file: {}'.format(self._outputfile))
        else:
            self.logger.debug('output file: empty')

        self._privkey = args.privkey
        if (args.privkey):
            self._privkey = args.privkey
            self.logger.debug('Private Key: {}'.format(self._privkey))
        else:
            self.logger.debug('Private Key empty')

        self._pubkey = args.pubkey
        if (args.pubkey):
            self._pubkey = args.pubkey
            self.logger.debug('Public Key: {}'.format(self._pubkey))
        else:
            self.logger.debug('Public Key empty')

        self._pwd = args.pwd
        if (args.pwd):
            self._pwd = args.pwd
            self.logger.debug('Password: {}'.format(self._pwd))
        else:
            self.logger.debug('Password empty')

        if (not retVal):
            ap.print_help()

        return retVal

    def generate_key(self):
        cryptor = CryptFile(self.logger)
        cryptor.generate_key(self._privkey, self._pubkey, self._pwd)
        
    def encrypt_file(self):
        cryptor = CryptFile(self.logger)
        cryptor.encrypt_file(self._inputfile, self._outputfile, self._pubkey)

    def decrypt_file(self):
        cryptor = CryptFile(self.logger)
        cryptor.decrypt_file(self._inputfile, self._outputfile, self._privkey, self._pwd)

    def run(self):
        if (self.parse_args()):
            if(self._command=='generate'):
                self.generate_key()
            elif(self._command=='encrypt'):
                self.encrypt_file()
            elif(self._command=='decrypt'):
                self.decrypt_file()
            else:
                self.logger.warning('Unknown command : {}'.format(self._command))

            self.logger.info('Job finished'.format(self._inputfile))
                
           
if __name__ == "__main__":
    runner = CrypterShell()
    runner.run()
