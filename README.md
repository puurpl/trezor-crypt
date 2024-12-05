# Trezor-Crypt  
  
At this point in thime this is nothing more than a project quickly slapped together with the help of AI. But it seems to work, and I will be further testing and developing it over time.  

## Purpose  
  
It provides a standardized way to use the trezor as a hardware store of keys to make use of cryptographic schemes which the trezore cannot.  
  
## Limitations  
  
The symmetrical key is generated and the encryption/decryption happens on the users system before the key value is overwritten. This means that even though the key is never saved and is immediately overwritten, the key could be stolen by an attacker and any intercepted or accessible encrypted data could be accessed.  
Of course this also shares the limitations of the trezor, associated libraries and encryption schemes used.  
  
## How to Use  
  
-- Download or copy this repo, or just the trezor-crypt.py  
-- Set up a virtual environment  
-- From within that environment install requirements.txt  
-- run trezor-crypt.py with the appropriate arguments  
  
## trezor-crypt man page  
  
Modes    -    Args  
-- encrypt - input-path output-path (options)  
-- decrypt - input-path output-path  
  
Options  
-- trezor-path - Trezor path to use for key derivation  
-- encryption - Encryption scheme (default: AES-GCM)  
  
The trezor-path and encryption-scheme get saved in metadata and used when running decrypt  
