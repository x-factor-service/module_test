from cryptography.fernet import Fernet
import json

def load_key():
    with open("secret.key", "rb") as key_file:
        key = key_file.read()
    return key

def decrypt_message(encrypted_message: bytes, key: bytes) -> str:
    """
    Decrypt a message
    """
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)
    return decrypted_message