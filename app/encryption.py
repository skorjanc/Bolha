from cryptography.fernet import Fernet
from .config import settings

def encrypt(password: str):
    fernet = Fernet(bytes(settings.encryption_key, 'utf-8'))
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password

def decrypt(password: str):
    fernet = Fernet(bytes(settings.encryption_key, 'utf-8'))
    decrypted_password = fernet.decrypt(password).decode()
    return decrypted_password