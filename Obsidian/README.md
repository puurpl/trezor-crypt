# Trezor-Crypt Obsidian

I made this program to encrypt my Obsidian repo for private storage, potentially on public media. For now a private GH repo though.  

The aim is to use my Trezor device to easily handle secure operations so that I can maintain a backup up yet secure copy of my Obsidian files, even if my local machines and storage are lost.  
This functionality skips the user confirming each encryption operation and instead simply asks for a password at the beginning (to derive the keys).  
Encryption happens onboard the Trezor device. And obviously a huge advantage of this is that the encyption is not the same for multiple operations, depending on the file path to derive the key for individual files and setting IVs to make it difficult to see which files have been changed from one commit to the next. Everything is derived deterministically and all relevant properties are stored in the header of the encrypted file. This allows the use of very secure and non-repeating keys while still being able to decrypt and recover everything simply by remembering the Seed Phrase and encryption password (which does accept an empty field).  

## Implemented

- Recursively encrypts an entire directory structure  
- Skips over .git directore and README.md (intended for the user to save necessary instructions to access the dir)  
- Stops operation on encrypt or decrypt error  
- Saves file hash in header and compares hash upon decryption, exits with warning if not a match  
- IGNORES: .git/ .gitignore Vault and README.md. Vault is intended for files requiring individual decryption with confirmation. (Not yet implemented)  
- 'temp' will be encrypted, but not pushed to repo ('temp/' should be in .gitignore)  

## Yet to Implement

- Handling for extra secure files requiring individual confirmation  
- Encrypting the header and filename for each file (in a single opening/closing operation for the entire dir)- possibly abstracting the entire filestructure during encryption.  
- Deniabililty and multiple domains, allow encryption operations to fail but not stop the process, meaning that more than one password could be utilized and only files encrypted to that password would be decrypted in a session. (Unless run multiple times with the passwords in questin) The problem in that case would be distinguishing which files belong to which domain for re-encryption.  

## Notes

- 16KB chunks were too much and caused locking up intermittently on decrypt, 1KB chunks seem ok, more testing needed. Can probably speed up process marginally with larger chunks.  
