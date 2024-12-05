# Trezor-Crypt

At this point in thime this is nothing more than a project quickly slapped together with the help of AI. But it seems to work, and I will be further testing and developing it over time.

## Purpose

It provides a standardized way to use the trezor as a hardware store of keys to make use of cryptographic schemes which the trezore cannot.

## Limitations

The symmetrical key is generated and the encryption/decryption happens on the users system before the key value is overwritten. This means that even though the key is never saved and is immediately overwritten, the key could be stolen by an attacker and any intercepted or accessible encrypted data could be accessed.
Of course this also shares the limitations of the trezor, associated libraries and encryption schemes used.
