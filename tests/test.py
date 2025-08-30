import os
import shutil
from src.cripto_manager import generate_key, load_key, InvalidKeyError
from src.sender import encrypt_message
from src.receiver import decrypt_message

def run_tests():
    print("\n=== TESTE 1: Chave válida, mensagem válida ===")
    if not os.path.exists("../key.key"):
        generate_key()
    key = load_key()
    msg = "Teste mensagem secreta"
    encrypted = encrypt_message(msg)
    decrypted = decrypt_message(encrypted)
    print(f"Mensagem original: {msg}")
    print(f"Mensagem descriptografada: {decrypted}")

    print("\n=== TESTE 2: Mensagem corrompida ===")
    encrypted_corrupt = encrypted[:-5] + b"12345"  # altera a mensagem criptografada
    result = decrypt_message(encrypted_corrupt)
    print(f"Resultado ao tentar descriptografar mensagem corrompida: {result}")

    print("\n=== TESTE 3: Chave corrompida ===")
    # Backup da chave válida
    shutil.copy("../key.key", "key_backup.key")

    # Corrompe a chave
    with open("../key.key", "wb") as f:
        f.write(b"chave_invalida")

    try:
        result = decrypt_message(encrypted)
        print(f"Resultado com chave corrompida: {result}")
    except InvalidKeyError as e:
        print(f"Erro detectado: {e}")

    # Restaura chave válida
    shutil.move("key_backup.key", "../key.key")

    print("\n=== TESTE 4: Chave válida mas mensagem não correspondente ===")
    # Cria nova chave (não vai bater com a mensagem anterior)
    generate_key()
    new_encrypted = encrypt_message("Outra mensagem")
    result = decrypt_message(encrypted)  # tenta descriptografar a antiga com nova chave
    print(f"Resultado: {result}")

    print("\n=== TODOS OS TESTES FINALIZADOS ===")

if __name__ == "__main__":
    run_tests()
