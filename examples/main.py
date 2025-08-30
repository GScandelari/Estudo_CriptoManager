import os
from src.cripto_manager import generate_key, load_key, InvalidKeyError
from src.sender import encrypt_message
from src.receiver import decrypt_message

# Caminho absoluto para a raiz do projeto
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
KEY_PATH = os.path.join(PROJECT_ROOT, "key.key")

def main():
    # Gera ou valida a chave
    if not os.path.exists(KEY_PATH):
        print("Nenhuma chave encontrada. Gerando uma nova...")
        generate_key(KEY_PATH)  # passamos o caminho completo
    else:
        try:
            load_key(KEY_PATH)     # passamos o caminho completo
            print("Chave existente validada com sucesso.")
        except InvalidKeyError as e:
            print(f"Erro: {e}")
            return

    # Entrada da mensagem
    msg = input("Digite a mensagem que deseja enviar: ")

    # Envia a mensagem (criptografia)
    encrypted = encrypt_message(msg, KEY_PATH)
    print(f"\nMensagem criptografada: {encrypted}")

    # Receiver (descriptografia)
    decrypted = decrypt_message(encrypted, KEY_PATH)
    print(f"Resultado: {decrypted}")

if __name__ == "__main__":
    main()
