from cryptography.fernet import Fernet, InvalidToken
from src.cripto_manager import load_key, InvalidKeyError

def decrypt_message(encrypted_message: bytes) -> str:
    """Descriptografa a mensagem com tratamento de chave inválida"""
    try:
        key = load_key()
        fernet = Fernet(key)
        decrypted = fernet.decrypt(encrypted_message)
        return decrypted.decode()
    except InvalidKeyError:
        return "Erro: chave armazenada em key.key não é válida."
    except InvalidToken:
        return "Mensagem não pode ser descriptografada, chave inválida."

if __name__ == "__main__":
    encrypted_msg = input("Cole a mensagem criptografada recebida: ").encode()
    decrypted_msg = decrypt_message(encrypted_msg)
    print(f"Resultado: {decrypted_msg}")
