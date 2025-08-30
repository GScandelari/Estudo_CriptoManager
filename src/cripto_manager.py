from cryptography.fernet import Fernet, InvalidToken
import os

class InvalidKeyError(Exception):
    pass

def generate_key(path="key.key"):
    """Gera uma nova chave e salva no caminho especificado"""
    key = Fernet.generate_key()
    with open(path, "wb") as key_file:
        key_file.write(key)
    print(f"Chave gerada e salva em {path}")

def load_key(path="key.key"):
    """Carrega a chave e valida se é Fernet"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Arquivo {path} não encontrado. Gere uma chave primeiro.")

    with open(path, "rb") as key_file:
        key = key_file.read()

    try:
        Fernet(key)
    except Exception:
        raise InvalidKeyError("A chave não é válida.")

    return key
