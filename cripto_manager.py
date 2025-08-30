from cryptography.fernet import Fernet, InvalidToken
import os

class InvalidKeyError(Exception):
    """Erro customizado para chave inválida"""
    pass

def generate_key():
    """Gera uma nova chave e salva em key.key"""
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)
    print("Chave gerada e salva em key.key")

def load_key():
    """Carrega a chave salva em key.key e valida se é uma chave Fernet"""
    if not os.path.exists("key.key"):
        raise FileNotFoundError("Arquivo key.key não encontrado. Gere uma chave com cripto_manager.py")

    with open("key.key", "rb") as key_file:
        key = key_file.read()

    # Valida se a chave realmente é uma chave Fernet
    try:
        Fernet(key)  # se for inválida, estoura ValueError
    except Exception:
        raise InvalidKeyError("A chave em key.key não é válida")

    return key

if __name__ == "__main__":
    generate_key()
