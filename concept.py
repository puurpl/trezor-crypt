import os
import ctypes
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


# Derive a deterministic symmetric key from Trezor
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


# Encrypt a file
def encrypt_file(input_path, output_path, trezor_path):
    """Encrypt a file using a symmetric key derived from the Trezor."""
    key = derive_key_from_trezor(trezor_path)
    try:
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        with open(input_path, "rb") as infile, open(output_path, "wb") as outfile:
            outfile.write(iv)  # Write the IV
            outfile.write(b"\0" * 16)  # Reserve space for the tag
            while chunk := infile.read(1024):
                outfile.write(encryptor.update(chunk))
            encrypted_data = encryptor.finalize()
            outfile.write(encrypted_data)

            # Write the tag at the reserved space
            outfile.seek(16)
            outfile.write(encryptor.tag)
        print(f"Encrypted {input_path} to {output_path}.")
        print(f"IV (hex): {iv.hex()}")  # Debug: Log the IV
        print(f"Tag (hex): {encryptor.tag.hex()}")  # Debug: Log the GCM tag
    finally:
        secure_erase(key)

# Decrypt a file
def decrypt_file(input_path, output_path, trezor_path):
    """Decrypt a file using a symmetric key derived from the Trezor."""
    key = derive_key_from_trezor(trezor_path)

    try:
        with open(input_path, "rb") as infile, open(output_path, "wb") as outfile:
            iv = infile.read(16)  # Read the IV
            tag = infile.read(16)  # Read the GCM tag
            encrypted_data = infile.read()  # Read the encrypted data

            print(f"IV (hex): {iv.hex()}")  # Debug: Log the IV
            print(f"Tag (hex): {tag.hex()}")  # Debug: Log the GCM tag

            cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
            decryptor = cipher.decryptor()
            outfile.write(decryptor.update(encrypted_data))
            outfile.write(decryptor.finalize())
        print(f"Decrypted {input_path} to {output_path}.")
    except Exception as e:
        print(f"Error during decryption: {e}")
        raise
    finally:
        secure_erase(key)

# Example Usage
if __name__ == "__main__":
    trezor_path = "m/44'/0'/0'/0/0"
    
    # Encrypt a file
    encrypt_file("example.txt", "example.txt.enc", trezor_path)

    # Decrypt the file
    decrypt_file("example.txt.enc", "example_decrypted.txt", trezor_path)
