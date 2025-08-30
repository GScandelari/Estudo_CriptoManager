import os
from cripto_manager import generate_key, load_key, InvalidKeyError
from sender import encrypt_message
from receiver import decrypt_message

def main():
    # Gera ou valida a chave
    if not os.path.exists("key.key"):
        print("Nenhuma chave encontrada. Gerando uma nova...")
        generate_key()
    else:
        try:
            load_key()
            print("Chave existente validada com sucesso.")
        except InvalidKeyError as e:
            print(f"Erro: {e}")
            return

    # Entrada da mensagem
    msg = input("Digite a mensagem que deseja enviar: ")

    # Envia a mensagem (criptografia)
    encrypted = encrypt_message(msg)
    print(f"\nMensagem criptografada: {encrypted}")

    # Receiver (descriptografia)
    decrypted = decrypt_message(encrypted)
    print(f"Resultado: {decrypted}")

if __name__ == "__main__":
    main()
