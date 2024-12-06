# Trezor-Crypt  
  
At this point in time this is nothing more than a project quickly slapped together with the help of AI. But it seems to work, and I will be further testing and developing it over time.  

## Background  
  
I wanted to encrypt some files to store them in the cloud, but I didn't want to create new keys and deal with securaly and safely storing and restoring them. Instead I created this protocol which leverages the trezor device to securely secure the data from which the key is derived to create the key on the fly and perform the cryptographic opeeration before securely overwriting the key in memory. This is not as secure as keeping the key and encryption operations withing the Trezor hardware, but it is as close as I can reasonably get and probably a lot faster.
  
## Purpose  
  
It provides a standardized way to use the trezor as a hardware store of keys to make use of cryptographic schemes which the trezor cannot. These keys are generated in a deterministic way from the trezor, used in the operation and then overwritten immediately. This doesn't keep the key as secure as it would be remaining on the trezor device, but perhaps more secure than saved somewhere on the system - and almost certainly easier to recover.
  
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
  
## Improvements  
  
Please see issues for the most complete list of pending improvements, but here are a few...  
-- GUI  
-- Wider range of encryption schemes  
-- Double layer encryption, preferrably allowing the final decryption to happen on the device  
-- Better error handling, providing appropriate error messages when the key is not the correct key etc  
-- Ability to us post-quantum asymmetrical encrytption  
