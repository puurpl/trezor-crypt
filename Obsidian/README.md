# Trezor-Crypt Obsidian

I made this program to encrypt my Obsidian repo for private storage, potentially on public media. For now a private GH repo though.

The aim is to use my Trezor device to easily handle secure operations so that I can maintain a backup up yet secure copy of my Obsidian files, even if my local machines and storage are lost.
This functionality skips the user confirming each encryption operation and instead simply asks for a password at the beginning.
Encryption happens onboard the Trezor device.

## Implemented

- Recursively encrypts an entire directory structure
- Skips over .git directore and README.md (intended for the user to save necessary instructions to access the dir)
- Stops operation on encrypt or decrypt error
- Saves file hash in header and compares hash upon decryption, exits with warning if not a match


## Yet to Implement

- Handling for extra secure files requiring individual confirmation
- Pass files through encryption in chunks, allowing larger file sizes
- Encrypting the header and filename for each file (in a single opening/closing operation for the entire dir)- possibly abstracting the entire filestructure during encryption. 

## Notes

- 16KB chunks were too much and caused locking up intermittently, 12KKB chunks seem ok
