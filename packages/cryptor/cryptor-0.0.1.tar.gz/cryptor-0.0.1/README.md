# Crypto Playground

Place for various test of crypto libs in python

## Sources

- [Python 3: An Intro to Encryption](https://www.blog.pythonlibrary.org/2016/05/18/python-3-an-intro-to-encryption/)
- [pycryptodome examples](https://pycryptodome.readthedocs.io/en/latest/src/examples.html)
- [Creating RSA Keys](https://www.tutorialspoint.com/cryptography_with_python/cryptography_with_python_creating_rsa_keys.htm)

## Installation

### Conda - Windows

``` bash
conda install -c conda-forge pycryptodomeex
```

### pip - Linux

- Get it from git

``` bash
cd ~/_projects/github/
git clone https://github.com/pavelsuk/crypto_playground crypto_playground
cd ~/_projects/github/crypto_playground
```

- Create virtual environment

``` bash
sudo apt install python3-venv
cd ~/_projects/github/crypto_playground
python3.6 -m venv env
source env/bin/activate
```

- Install packages

``` bash
cd ~/_projects/github/crypto_playground
git fetch
git merge
source env/bin/activate
pip install -r requirements.txt
```

## Usage

### Generate key pair

``` bash
# generate private_key.pem (without password) and public_key.pem:
python cryptorshell.py generate

# generate key pair (password protected) to specific files:
python cryptorshell.py generate --privkey private_pwd.pem --pubkey public_pwd.pem --pwd mylittlesecretpwd
```

### Encrypt & Decrypt file

``` bash
# encrypt little_secret.txt to little_secret.txt.encrypted using default public_key.pem
python cryptorshell.py encrypt little_secret.txt

# decrypt little_secret.txt.encrypted to little_secret.txt.dec using default public_key.pem
python cryptorshell.py decrypt little_secret.txt.encrypted little_secret.txt.dec

# encrypt file little_secret.txt to encrypted_secret.enc  using public key public_pwd.pem
python cryptorshell.py encrypt little_secret.txt encrypted_secret.enc --pubkey public_pwd.pem

# decrypt encrypted_secret.enc to encrypted_secret.dec using password protected private key
python cryptorshell.py decrypt encrypted_secret.enc decrypted_secret.dec --privkey private_pwd.pem --pwd mylittlesecretpwd

```
