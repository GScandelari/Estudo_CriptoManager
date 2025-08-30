import os
import shutil
from src.cripto_manager import generate_key, load_key, InvalidKeyError
from src.sender import encrypt_message
from src.receiver import decrypt_message

# Caminho absoluto para a raiz do projeto
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
KEY_PATH = os.path.join(PROJECT_ROOT, "key.key")

def run_tests():
    print("\n=== TESTE 1: Chave válida, mensagem válida ===")
    if not os.path.exists(KEY_PATH):
        generate_key(KEY_PATH)
    key = load_key(KEY_PATH)
    msg = "Teste mensagem secreta"
    encrypted = encrypt_message(msg, KEY_PATH)
    decrypted = decrypt_message(encrypted, KEY_PATH)
    print(f"Mensagem original: {msg}")
    print(f"Mensagem descriptografada: {decrypted}")

    print("\n=== TESTE 2: Mensagem corrompida ===")
    encrypted_corrupt = encrypted[:-5] + b"12345"  # altera a mensagem criptografada
    result = decrypt_message(encrypted_corrupt, KEY_PATH)
    print(f"Resultado ao tentar descriptografar mensagem corrompida: {result}")

    print("\n=== TESTE 3: Chave corrompida ===")
    # Backup da chave válida
    backup_path = os.path.join(PROJECT_ROOT, "key_backup.key")
    shutil.copy(KEY_PATH, backup_path)

    # Corrompe a chave
    with open(KEY_PATH, "wb") as f:
        f.write(b"chave_invalida")

    result = decrypt_message(encrypted, KEY_PATH)
    print(f"Resultado com chave corrompida: {result}")

    # Restaura chave válida
    shutil.move(backup_path, KEY_PATH)

    print("\n=== TESTE 4: Chave válida mas mensagem não correspondente ===")
    # Cria nova chave (não vai bater com a mensagem anterior)
    generate_key(KEY_PATH)
    new_encrypted = encrypt_message("Outra mensagem", KEY_PATH)
    result = decrypt_message(encrypted, KEY_PATH)  # tenta descriptografar a antiga com nova chave
    print(f"Resultado: {result}")

    print("\n=== TODOS OS TESTES FINALIZADOS ===")

if __name__ == "__main__":
    run_tests()
