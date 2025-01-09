import argparse
import os
import hashlib
import logging
from trezorlib.client import TrezorClient
from trezorlib.misc import encrypt_keyvalue, decrypt_keyvalue
from trezorlib.tools import parse_path
from trezorlib.transport import get_transport
from trezorlib.ui import ClickUI

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

DEFAULT_PATH = "m/10011'/0'"

def read_file(file_path):
    logging.debug(f"Reading file: {file_path}")
    with open(file_path, "rb") as f:
        return f.read()

def write_file(file_path, data):
    logging.debug(f"Writing file: {file_path}")
    with open(file_path, "wb") as f:
        f.write(data)

def delete_file(file_path):
    logging.debug(f"Deleting file: {file_path}")
    os.remove(file_path)

def pad(data):
    padding_size = 16 - (len(data) % 16)
    logging.debug(f"Padding size: {padding_size}")
    return data + bytes([padding_size] * padding_size)

def unpad(data):
    padding_size = data[-1]
    logging.debug(f"Unpadding size: {padding_size}")
    return data[:-padding_size]

def encrypt(client, path, key, value):
    logging.debug(f"Encrypting with key: {key} and path: {path}")
    address_n = parse_path(path)
    padded_value = pad(value)
    return encrypt_keyvalue(client, address_n, key, padded_value, ask_on_encrypt=False, ask_on_decrypt=False)

def decrypt(client, path, key, value):
    logging.debug(f"Decrypting with key: {key} and path: {path}")
    address_n = parse_path(path)
    decrypted_value = decrypt_keyvalue(client, address_n, key, value, ask_on_encrypt=False, ask_on_decrypt=False)
    return unpad(decrypted_value)

def compute_hash(data):
    file_hash = hashlib.sha256(data).hexdigest()
    logging.debug(f"Computed hash: {file_hash}")
    return file_hash

def process_file(client, file_path, base_dir, action, path):
    relative_path = os.path.relpath(file_path, base_dir)
    key = relative_path[:-4] if action == "decrypt" and relative_path.endswith(".enc") else relative_path
    logging.debug(f"Processing file: {file_path} with relative path: {relative_path} and action: {action}")
    if action == "encrypt":
        data = read_file(file_path)
        file_hash = compute_hash(data)
        encrypted_data = encrypt(client, path, key, data)
        header = f"{file_hash}\n".encode()  # Add hash to header
        write_file(file_path + ".enc", header + encrypted_data)
        delete_file(file_path)  # Remove the original file after encryption
    elif action == "decrypt":
        data = read_file(file_path)
        header, encrypted_data = data.split(b'\n', 1)
        file_hash = header.decode()
        decrypted_data = decrypt(client, path, key, encrypted_data)
        if compute_hash(decrypted_data) != file_hash:
            logging.error(f"Hash mismatch for {file_path}, decryption aborted.")
            return
        write_file(file_path.replace(".enc", ""), decrypted_data)
        delete_file(file_path)  # Remove the encrypted file after successful decryption

def process_directory(client, directory, action, path):
    logging.debug(f"Processing directory: {directory} with action: {action}")
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if (action == "encrypt" and not file_path.endswith(".enc")) or \
               (action == "decrypt" and file_path.endswith(".enc")):
                process_file(client, file_path, directory, action, path)

def main():
    parser = argparse.ArgumentParser(description="Encrypt or Decrypt an entire directory using Trezor.")
    parser.add_argument("directory", help="Directory to encrypt/decrypt")
    parser.add_argument("--path", help="BIP-32 path", default=DEFAULT_PATH)
    parser.add_argument("--action", choices=["encrypt", "decrypt"], required=True, help="Action to perform: encrypt or decrypt")
    args = parser.parse_args()

    logging.debug(f"Arguments: {args}")

    transport = get_transport()
    client = TrezorClient(transport, ui=ClickUI())

    process_directory(client, args.directory, args.action, args.path)

    client.close()

if __name__ == "__main__":
    main()
