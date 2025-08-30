import os
from datetime import datetime
from typing import Tuple
from src.key_store import key_path_for, has_key_for
from src.cripto_manager import load_key, InvalidKeyError
from src.receiver import decrypt_message

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LOG_PATH = os.path.join(PROJECT_ROOT, "messages.log")
DISPLAY_PATH = os.path.join(PROJECT_ROOT, "display.txt")

def format_display_line(timestamp: datetime, sender_id: str, encrypted_bytes: bytes) -> str:
    ts = timestamp.strftime("%Y-%m-%d_%H-%M-%S")
    # dois underscores entre timestamp e ID para ficar como no seu exemplo
    return f"{ts}__{sender_id}: {encrypted_bytes!r}"

def append_message_log(sender_id: str, encrypted_bytes: bytes, timestamp: datetime = None):
    if timestamp is None:
        timestamp = datetime.now()
    line = format_display_line(timestamp, sender_id, encrypted_bytes)
    # salva no log bruto (apêndice)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    # atualiza o display público (poderíamos reescrever inteiro, aqui apenas append)
    with open(DISPLAY_PATH, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    return line

def list_display_lines() -> list:
    if not os.path.exists(DISPLAY_PATH):
        return []
    with open(DISPLAY_PATH, "r", encoding="utf-8") as f:
        return [l.rstrip("\n") for l in f]

def parse_display_line(line: str) -> Tuple[str, str, bytes]:
    """
    Retorna (timestamp_str, sender_id, encrypted_bytes)
    Exemplo de linha:
    2025-08-30_16-37-01__ID_A: b'....'
    """
    try:
        ts_and_rest = line.split("__", 1)
        ts_str = ts_and_rest[0]
        rest = ts_and_rest[1]
        sender_id, enc_repr = rest.split(":", 1)
        sender_id = sender_id.strip()
        enc_repr = enc_repr.strip()
        # avaliar repr de bytes com literal_eval é mais seguro que eval
        import ast
        encrypted_bytes = ast.literal_eval(enc_repr)
        return ts_str, sender_id, encrypted_bytes
    except Exception as e:
        raise ValueError(f"Linha inválida: {line}") from e

def try_decrypt_line_for_sender(line: str, sender_id: str) -> Tuple[str, str]:
    """
    Tenta descriptografar a linha com a chave do sender_id.
    Retorna (status, message) onde status = "ok" | "encrypted" | "no-key" | "invalid-key"
    """
    try:
        ts_str, line_sender, encrypted = parse_display_line(line)
    except ValueError:
        return "invalid-line", line

    if line_sender != sender_id:
        return "not-target", line  # não é para esse sender_id

    # Verifica se temos a chave para esse sender
    if not has_key_for(sender_id):
        return "no-key", line

    try:
        # load_key_for equivale a load_key(path)
        key_path = key_path_for(sender_id)
        key = load_key(key_path)
    except FileNotFoundError:
        return "no-key", line
    except InvalidKeyError:
        return "invalid-key", "Chave inválida para " + sender_id

    # Tentar descriptografar com a chave
    try:
        # decrypt_message espera bytes e um key_path na nossa versão; usamos load_key direto e Fernet aqui:
        from cryptography.fernet import Fernet, InvalidToken
        f = Fernet(key)
        plaintext = f.decrypt(encrypted)
        return "ok", plaintext.decode()
    except Exception as e:
        # InvalidToken ou qualquer outro -> manter criptografado
        return "encrypted", line
