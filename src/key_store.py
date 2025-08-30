import os
from src.cripto_manager import generate_key, load_key, InvalidKeyError

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
KEY_DIR = os.path.join(PROJECT_ROOT, "keys")
os.makedirs(KEY_DIR, exist_ok=True)

def key_path_for(sender_id: str) -> str:
    # safe file name
    fname = f"{sender_id}.key"
    return os.path.join(KEY_DIR, fname)

def generate_key_for(sender_id: str) -> str:
    path = key_path_for(sender_id)
    generate_key(path)
    return path

def load_key_for(sender_id: str) -> bytes:
    path = key_path_for(sender_id)
    return load_key(path)  # pode lançar FileNotFoundError ou InvalidKeyError

def has_key_for(sender_id: str) -> bool:
    return os.path.exists(key_path_for(sender_id))
