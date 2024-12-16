import os
import ctypes
import json
import argparse
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from trezorlib.client import TrezorClient
from trezorlib.transport import get_transport
from trezorlib.ui import ClickUI
from trezorlib import btc
from trezorlib import tools

def secure_erase(data):
    """Overwrite data in memory."""
    if isinstance(data, (bytes, bytearray)):
        mutable_data = bytearray(data)  # Convert to mutable type
        ptr = ctypes.cast(id(mutable_data), ctypes.POINTER(ctypes.c_char * len(mutable_data)))
        ctypes.memset(ptr, 0, len(mutable_data))
        del mutable_data  # Explicitly delete mutable copy
    else:
        raise ValueError("Data must be a bytes or bytearray object.")

def derive_key_from_trezor(path):
    """Derive a 256-bit AES key from the Trezor seed."""
    transport = get_transport()
    client = TrezorClient(transport, ui=ClickUI())  # Attach UI for Trezor interaction
    
    # Convert path string to list of integers
    path_list = tools.parse_path(path)
    
    # Get public node for the path
    node = btc.get_public_node(client, path_list).node
    public_key = node.public_key.hex()
    
    # Hash the public key to create a 256-bit symmetric key
    key = bytearray(public_key.encode()[:32])  # Convert to mutable bytearray
    return key

def write_metadata(outfile, metadata):
    """Write metadata as JSON with length prefix."""
    metadata_json = json.dumps(metadata).encode()
    metadata_length = len(metadata_json)
    outfile.write(metadata_length.to_bytes(4, "big"))  # Write metadata length
    outfile.write(metadata_json)  # Write metadata JSON

def read_metadata(infile):
    """Read metadata as JSON from file."""
    metadata_length = int.from_bytes(infile.read(4), "big")  # Read metadata length
    metadata_json = infile.read(metadata_length).decode()  # Read metadata JSON
    return json.loads(metadata_json)

def encrypt_file(input_path, output_path, trezor_path):
    """Encrypt a file using a symmetric key derived from the Trezor."""
    key = derive_key_from_trezor(trezor_path)
    metadata = {"trezor_path": trezor_path, "encryption": "AES-GCM"}
    try:
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        with open(input_path, "rb") as infile, open(output_path, "wb") as outfile:
            write_metadata(outfile, metadata)  # Write metadata to the file
            outfile.write(iv)  # Write the IV
            outfile.write(b"\0" * 16)  # Reserve space for the tag
            while chunk := infile.read(1024):
                outfile.write(encryptor.update(chunk))
            encrypted_data = encryptor.finalize()
            outfile.write(encrypted_data)

            # Write the tag at the reserved space
            outfile.seek(4 + len(json.dumps(metadata)) + 16)
            outfile.write(encryptor.tag)
        print(f"Encrypted {input_path} to {output_path}.")
    finally:
        secure_erase(key)

def decrypt_file(input_path, output_path, trezor_path):
    """Decrypt a file using a symmetric key derived from the Trezor."""
    with open(input_path, "rb") as infile:
        metadata = read_metadata(infile)  # Read metadata from the file
        print(f"Metadata: {metadata}")

        if metadata["trezor_path"] != trezor_path:
            print("Trezor path mismatch! Using path from metadata.")
            trezor_path = metadata["trezor_path"]
        
        key = derive_key_from_trezor(trezor_path)
        try:
            iv = infile.read(16)  # Read the IV
            tag = infile.read(16)  # Read the GCM tag
            encrypted_data = infile.read()  # Read the encrypted data

            cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
            decryptor = cipher.decryptor()
            with open(output_path, "wb") as outfile:
                outfile.write(decryptor.update(encrypted_data))
                outfile.write(decryptor.finalize())
            print(f"Decrypted {input_path} to {output_path}.")
        except Exception as e:
            print(f"Error during decryption: {e}")
            raise
        finally:
            secure_erase(key)
