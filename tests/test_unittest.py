import os
import shutil
import unittest
from src.cripto_manager import generate_key, load_key, InvalidKeyError
from src.sender import encrypt_message
from src.receiver import decrypt_message

class TestCryptoSystem(unittest.TestCase):

    def setUp(self):
        # Garante sempre começar com uma chave válida
        if os.path.exists("key.key"):
            os.remove("key.key")
        generate_key()

    def test_valid_message(self):
        """Mensagem deve ser criptografada e descriptografada corretamente"""
        msg = "Mensagem secreta"
        encrypted = encrypt_message(msg)
        decrypted = decrypt_message(encrypted)
        self.assertEqual(msg, decrypted)

    def test_corrupted_message(self):
        """Mensagem alterada não pode ser descriptografada"""
        msg = "Teste"
        encrypted = encrypt_message(msg)
        encrypted_corrupt = encrypted[:-5] + b"12345"  # corrompe mensagem
        result = decrypt_message(encrypted_corrupt)
        self.assertIn("chave inválida", result)

    def test_corrupted_key(self):
        """Chave inválida deve ser detectada"""
        msg = "Teste"
        encrypted = encrypt_message(msg)

        # Backup da chave válida
        shutil.copy("key.key", "key_backup.key")

        # Corrompe a chave
        with open("key.key", "wb") as f:
            f.write(b"xxx_invalido_xxx")

        result = decrypt_message(encrypted)
        self.assertIn("chave", result.lower())

        # Restaura chave válida
        shutil.move("key_backup.key", "key.key")

    def test_key_not_matching_message(self):
        """Mensagem antiga não deve ser descriptografada com nova chave"""
        msg = "Primeira"
        encrypted = encrypt_message(msg)

        # Gera nova chave que não bate com a mensagem antiga
        generate_key()
        result = decrypt_message(encrypted)
        self.assertIn("chave inválida", result)

if __name__ == "__main__":
    unittest.main()
