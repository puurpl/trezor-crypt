# Trezor-Crypt  
  
PLEASE DON'T TRUST THIS PROJECT WITH ANY VALUABLE SECRETS FOR THE MOMENT. iT HAS NOT BEEN AUDITED OR TESTED PROPERLY, NOT EVEN BY MYSELF.

## Background  
  
I wanted to encrypt some files to store them in the cloud, but I didn't want to create new keys and deal with securely storing and restoring them. So I created this protocol which leverages the trezor device and Satoshi Labs open source code to encrypt and decrypt on the device itself, or to generate the data (on the trezor) from which the key is derived to create the key on the fly and perform the cryptographic opeeration before securely overwriting the key in memory. This is not as secure as keeping the key and encryption operations withing the Trezor hardware, but it is as close as I can reasonably get and probably a lot faster, and it enables encryption schemes that would not otherwise be possible on the trezor device.
  
## Purpose  

The purpose of this project is to make my secure use of the trezor (relatively) effortless and effortlessly deterministic and recoverable. I am aware of much of Satoshi Labs own code and will be referring to and using their standards everywhere possible but not necessarily strictly adhering to them. 

SLIP11 - Is used in this project to encrypt/decrypt on the device a keyvalue pair.
  
## Limitations  
  

## How to Use  
  
-- Download or copy this repo, or just the trezor-crypt.py  
-- Set up a virtual environment  
-- From within that environment install requirements.txt  
-- run trezor-crypt.py with the appropriate arguments  
  
## trezor-crypt man page  
  

## Improvements  
  
Please see issues for the most complete list of pending improvements, but here are a few...  
-- Implement key encapsulation in header if file is greater than 16kb - my test files were all successful below 20kb, and 20 itself was mixed.  
-- GUI  
-- Wider range of encryption schemes  
-- Double layer encryption, preferrably allowing the final decryption to happen on the device  
-- Better error handling, providing appropriate error messages when the key is not the correct key etc  
-- Ability to use post-quantum asymmetrical encrytption  
