import argparse
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from pathlib import Path


key = bytes([0x32, 0x44, 0x6e, 0xca, 0xd9, 0x5c, 0x42, 0x9e, 0xeb, 0x33, 0xb9, 0x61, 0x9d, 0x8f, 0x52, 0x30, 0xdd, 0x8, 0x85, 0xb4, 0x78, 0x69, 0x8c, 0x65, 0x30, 0x2d, 0x9c, 0x4a, 0x6e, 0x51, 0xe2, 0x17])

# Function to encrypt a file
def encrypt_file(input_file, output_file, key, iv):
    # Initialize cipher
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Read the plaintext file
    with open(input_file, 'rb') as f:
        plaintext = f.read()

    # Apply PKCS7 padding to ensure the data is a multiple of the block size
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    # Encrypt the data
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    # Write the IV followed by the ciphertext to the output file
    with open(output_file, 'wb') as f:
        f.write(iv + ciphertext)


# Function to decrypt a file
def decrypt_file(input_file, output_file, key):
    # Read the IV and ciphertext from the input file
    with open(input_file, 'rb') as f:
        iv = f.read(16)  # AES block size is 16 bytes
        ciphertext = f.read()

    # Initialize cipher
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the data
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    # Remove padding
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    # Write the plaintext to the output file
    with open(output_file, 'wb') as f:
        f.write(plaintext)


def main():
    parser = argparse.ArgumentParser(description='Encrypt the given file')
    parser.add_argument('filename', help='File to encrypt')
    args = parser.parse_args()

    iv = os.urandom(16)  # Generate a random initialization vector

    basename = Path(args.filename).with_suffix('')

    # Encrypt the file
    encrypt_file(f'{basename}.whl', f'{basename}.ewhl', key, iv)


if __name__ == '__main__':
    main()
