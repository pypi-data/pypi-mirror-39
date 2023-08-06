import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cryptor",
    version="0.0.1",
    author="Pavel Suk",
    author_email="suk.pavel@gmail.com",
    description="Simple tool for encrypting and decrypting files with RSA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pavelsuk/cryptor",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)