from src.cripto_manager import load_key, InvalidKeyError
from cryptography.fernet import Fernet, InvalidToken

def decrypt_message(encrypted_message: bytes, key_path="key.key") -> str:
    try:
        key = load_key(key_path)
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
