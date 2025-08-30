from src.cripto_manager import load_key
from cryptography.fernet import Fernet

def encrypt_message(message: str, key_path="key.key") -> bytes:
    key = load_key(key_path)
    fernet = Fernet(key)
    return fernet.encrypt(message.encode())


if __name__ == "__main__":
    msg = input("Digite a mensagem para enviar: ")
    encrypted_msg = encrypt_message(msg)
    print(f"Mensagem criptografada (enviar ao receiver): {encrypted_msg}")
