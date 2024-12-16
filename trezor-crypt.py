import argparse
import os
import json
from trezorlib.client import TrezorClient
from trezorlib.misc import encrypt_keyvalue, decrypt_keyvalue
from trezorlib.tools import parse_path
from trezorlib.transport import get_transport
from trezorlib.ui import ClickUI
from ./extended import encrypt_file as extended_encrypt_file
from ./extended import encrypt_file as extended_decrypt_file

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

def encrypt(client, path, key, value, iv):
    address_n = parse_path(path)
    padded_value = pad(value)
    return encrypt_keyvalue(client, address_n, key, padded_value, iv=iv)

def decrypt(client, path, key, value, iv):
    address_n = parse_path(path)
    decrypted_value = decrypt_keyvalue(client, address_n, key, value, iv=iv)
    return unpad(decrypted_value)

def main():
    parser = argparse.ArgumentParser(description="Encrypt or Decrypt files using Trezor.")
    parser.add_argument("file", help="File to encrypt/decrypt")
    parser.add_argument("--key", help="Key value for encryption/decryption", default=None)
    parser.add_argument("--path", help="BIP-32 path", default=DEFAULT_PATH)
    parser.add_argument("--iv", help="Initialization vector", default=b"")
    parser.add_argument("--output", help="Output file location", default=None)
	parser.add_argument("--encryption", default="Onboard", help="Encryption scheme (default: Onboard)")
    args = parser.parse_args()

    transport = get_transport()
    client = TrezorClient(transport, ui=ClickUI())

    file_path = args.file
    output_path = args.output if args.output else file_path + ".enc" if not file_path.endswith(".enc") else file_path.replace(".enc", "")

    if file_path.endswith(".enc"):
		if args.encryption == "Onboard" || args.encryption == "": 
	        with open(file_path, "rb") as f:
	            header = json.loads(f.readline().decode())
	            data = f.read()
	        key = header['key']
	        decrypted_data = decrypt(client, header['path'], key, data, iv=args.iv)
	        write_file(output_path, decrypted_data)
		else
			extended_encrypt_file(args.input, args.output, args.trezor_path)
    else:
        key = args.key if args.key else f"Encrypt/Decrypt: {os.path.basename(file_path)}"
		if args.encryption == "Onboard" || args.encryption == "": 
	        data = read_file(file_path)
	        encrypted_data = encrypt(client, args.path, key, data, iv=args.iv)
	        header = {
	            'path': args.path,
	            'key': key,
	        }
	        with open(output_path, "wb") as f:
	            f.write(json.dumps(header).encode() + b"\n")
	            f.write(encrypted_data)
		else
			extended_decrypt_file(args.input, args.output, args.trezor_path)

    client.close()

if __name__ == "__main__":
    main()
