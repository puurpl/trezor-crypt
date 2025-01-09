import argparse
import os
from trezorlib.client import TrezorClient
from trezorlib.misc import encrypt_keyvalue, decrypt_keyvalue
from trezorlib.tools import parse_path
from trezorlib.transport import get_transport
from trezorlib.ui import ClickUI

DEFAULT_PATH = "m/10011'/0'"

def read_file(file_path):
    with open(file_path, "rb") as f:
        return f.read()

def write_file(file_path, data):
    with open(file_path, "wb") as f:
        f.write(data)

def pad(data):
    padding_size = 16 - (len(data) % 16)
    return data + bytes([padding_size] * padding_size)

def unpad(data):
    padding_size = data[-1]
    return data[:-padding_size]

def encrypt(client, path, key, value):
    address_n = parse_path(path)
    padded_value = pad(value)
    return encrypt_keyvalue(client, address_n, key, padded_value, ask_on_encrypt=False, ask_on_decrypt=False)

def decrypt(client, path, key, value):
    address_n = parse_path(path)
    decrypted_value = decrypt_keyvalue(client, address_n, key, value, ask_on_encrypt=False, ask_on_decrypt=False)
    return unpad(decrypted_value)

def process_file(client, file_path, base_dir, action, path):
    relative_path = os.path.relpath(file_path, base_dir)
    key = relative_path
    if action == "encrypt":
        data = read_file(file_path)
        encrypted_data = encrypt(client, path, key, data)
        write_file(file_path + ".enc", encrypted_data)
    elif action == "decrypt":
        data = read_file(file_path)
        decrypted_data = decrypt(client, path, key[:-4], data)
        write_file(file_path.replace(".enc", ""), decrypted_data)

def process_directory(client, directory, action, path):
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

    transport = get_transport()
    client = TrezorClient(transport, ui=ClickUI())

    process_directory(client, args.directory, args.action, args.path)

    client.close()

if __name__ == "__main__":
    main()
