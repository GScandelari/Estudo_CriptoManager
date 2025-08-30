from cryptography.fernet import Fernet
from src.cripto_manager import load_key

def encrypt_message(message: str) -> bytes:
    """Criptografa a mensagem usando a chave salva"""
    key = load_key()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(message.encode())
    return encrypted

if __name__ == "__main__":
    msg = input("Digite a mensagem para enviar: ")
    encrypted_msg = encrypt_message(msg)
    print(f"Mensagem criptografada (enviar ao receiver): {encrypted_msg}")
