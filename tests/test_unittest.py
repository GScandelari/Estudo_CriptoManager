import os
import shutil
import unittest
from src.cripto_manager import generate_key, load_key, InvalidKeyError
from src.sender import encrypt_message
from src.receiver import decrypt_message

# Caminho absoluto da chave na raiz do projeto
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
KEY_PATH = os.path.join(PROJECT_ROOT, "key.key")

class TestCryptoSystem(unittest.TestCase):

    def setUp(self):
        # Sempre começar com uma chave válida na raiz
        if os.path.exists(KEY_PATH):
            os.remove(KEY_PATH)
        generate_key(KEY_PATH)

    def test_valid_message(self):
        """Mensagem deve ser criptografada e descriptografada corretamente"""
        msg = "Mensagem secreta"
        encrypted = encrypt_message(msg, KEY_PATH)
        decrypted = decrypt_message(encrypted, KEY_PATH)
        self.assertEqual(msg, decrypted)

    def test_corrupted_message(self):
        """Mensagem alterada não pode ser descriptografada"""
        msg = "Teste"
        encrypted = encrypt_message(msg, KEY_PATH)
        encrypted_corrupt = encrypted[:-5] + b"12345"  # corrompe mensagem
        result = decrypt_message(encrypted_corrupt, KEY_PATH)
        self.assertIn("chave inválida", result)

    def test_corrupted_key(self):
        """Chave inválida deve ser detectada"""
        msg = "Teste"
        encrypted = encrypt_message(msg, KEY_PATH)

        # Backup da chave válida
        backup_path = KEY_PATH + ".bak"
        shutil.copy(KEY_PATH, backup_path)

        # Corrompe a chave
        with open(KEY_PATH, "wb") as f:
            f.write(b"xxx_invalido_xxx")

        result = decrypt_message(encrypted, KEY_PATH)
        self.assertIn("chave", result.lower())

        # Restaura chave válida
        shutil.move(backup_path, KEY_PATH)

    def test_key_not_matching_message(self):
        """Mensagem antiga não deve ser descriptografada com nova chave"""
        msg = "Primeira"
        encrypted = encrypt_message(msg, KEY_PATH)

        # Gera nova chave que não bate com a mensagem antiga
        generate_key(KEY_PATH)
        result = decrypt_message(encrypted, KEY_PATH)
        self.assertIn("chave inválida", result)

if __name__ == "__main__":
    unittest.main()
