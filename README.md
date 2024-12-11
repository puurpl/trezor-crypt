# Trezor-Crypt  
  
At this point in time this is nothing more than a project quickly slapped together with the help of AI. But it seems to work, and I will be further testing and developing it over time.  

## Background  
  
I wanted to encrypt some files to store them in the cloud, but I didn't want to create new keys and deal with securaly and safely storing and restoring them. Instead I created this protocol which leverages the trezor device to securely secure the data from which the key is derived to create the key on the fly and perform the cryptographic opeeration before securely overwriting the key in memory. This is not as secure as keeping the key and encryption operations withing the Trezor hardware, but it is as close as I can reasonably get and probably a lot faster.
  
## Purpose  

The purpose of this project is to make my secure use of the trezor (relatively) effortless and effortlessly deterministic and recoverable. I am aware of much of Satoshi Labs own code and will be referring to and using their standards everywhere possible but not necessarily strictly adhering to them. 

  
## Limitations  
  

## How to Use  
  
-- Download or copy this repo, or just the trezor-crypt.py  
-- Set up a virtual environment  
-- From within that environment install requirements.txt  
-- run trezor-crypt.py with the appropriate arguments  
  
## trezor-crypt man page  
  

## Improvements  
  
Please see issues for the most complete list of pending improvements, but here are a few...  
-- GUI  
-- Wider range of encryption schemes  
-- Double layer encryption, preferrably allowing the final decryption to happen on the device  
-- Better error handling, providing appropriate error messages when the key is not the correct key etc  
-- Ability to us post-quantum asymmetrical encrytption  
