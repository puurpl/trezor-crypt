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
CHUNK_SIZE = 1024 * 1  # 1KB

def read_file_in_chunks(file_path, chunk_size=CHUNK_SIZE):
    logging.debug(f"Reading file in chunks: {file_path}")
    with open(file_path, "rb") as f:
        while chunk := f.read(chunk_size):
            yield chunk

def write_file_in_chunks(file_path, data_chunks):
    logging.debug(f"Writing file in chunks: {file_path}")
    with open(file_path, "wb") as f:
        for chunk in data_chunks:
            f.write(chunk)

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

def encrypt_chunk(client, path, key, chunk):
    address_n = parse_path(path)
    padded_chunk = pad(chunk)
    return encrypt_keyvalue(client, address_n, key, padded_chunk, ask_on_encrypt=False, ask_on_decrypt=False)

def decrypt_chunk(client, path, key, chunk):
    address_n = parse_path(path)
    decrypted_chunk = decrypt_keyvalue(client, address_n, key, chunk, ask_on_encrypt=False, ask_on_decrypt=False)
    return unpad(decrypted_chunk)

def compute_hash(data):
    file_hash = hashlib.sha256(data).hexdigest()
    logging.debug(f"Computed hash: {file_hash}")
    return file_hash

def process_file(client, file_path, base_dir, action, path):
    relative_path = os.path.relpath(file_path, base_dir)
    key = relative_path[:-4] if action == "decrypt" and relative_path.endswith(".enc") else relative_path
    logging.debug(f"Processing file: {file_path} with relative path: {relative_path} and action: {action}")
    if action == "encrypt":
        file_data = read_file(file_path)
        file_hash = compute_hash(file_data)
        header = f"{file_hash}\n".encode()
        encrypted_chunks = []
        is_empty = True
        for chunk in read_file_in_chunks(file_path):
            is_empty = False
            encrypted_chunks.append(encrypt_chunk(client, path, key, chunk))
        if is_empty:
            logging.debug(f"Skipping encryption for empty file: {file_path}")
            return
        write_file_in_chunks(file_path + ".enc", [header] + encrypted_chunks)
        delete_file(file_path)  # Remove the original file after encryption
    elif action == "decrypt":
        with open(file_path, "rb") as f:
            header = f.readline().strip()
            file_hash = header.decode()
            encrypted_chunks = [f.read()]
        if not encrypted_chunks[0]:
            logging.debug(f"Skipping decryption for empty file: {file_path}")
            return
        decrypted_chunks = []
        for chunk in encrypted_chunks:
            decrypted_chunks.append(decrypt_chunk(client, path, key, chunk))
        decrypted_data = b''.join(decrypted_chunks)
        logging.debug(f"File Hash: {file_hash}\nDecrypted Data Hash: {compute_hash(decrypted_data)}")
        if compute_hash(decrypted_data) != file_hash:
            logging.error(f"Hash mismatch for {file_path}, decryption aborted.")
            raise ValueError(f"Hash mismatch for {file_path}")
        write_file_in_chunks(file_path.replace(".enc", ""), decrypted_chunks)
        delete_file(file_path)  # Remove the encrypted file after successful decryption

def process_directory(client, directory, action, path):
    logging.debug(f"Processing directory: {directory} with action: {action}")
    for root, dirs, files in os.walk(directory):
        # Skip the .git directory
        if '.git' in dirs:
            dirs.remove('.git')
        if '.gitignore' in files:
            files.remove('.gitignore')
        if 'README.md' in files:
            files.remove('README.md')
        if (action == "decrypt" and 'Vault' in dirs):
            dirs.remove('Vault')
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

    try:
        process_directory(client, args.directory, args.action, args.path)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()
