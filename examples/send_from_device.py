import sys
import os
from datetime import datetime
from src.key_store import has_key_for, generate_key_for, key_path_for
from src.cripto_manager import load_key
from src.sender import encrypt_message
from src.controller import append_message_log

def send(sender_id: str, message: str):
    # garante que exista chave para o sender (se quiser que a central gere, remova esta linha)
    if not has_key_for(sender_id):
        print(f"Nenhuma chave para {sender_id}. Gerando nova chave em keys/{sender_id}.key")
        generate_key_for(sender_id)

    key_path = key_path_for(sender_id)
    # encrypt_message espera message + key_path (conforme alteração anterior)
    encrypted = encrypt_message(message, key_path)
    line = append_message_log(sender_id, encrypted, datetime.now())
    print("Mensagem enviada e adicionada ao display:")
    print(line)

if __name__ == "__main__":
    # exemplo: python send_from_device.py ID_A "Olá mundo"
    if len(sys.argv) < 3:
        print("Usage: python send_from_device.py <SENDER_ID> <MESSAGE>")
    else:
        send(sys.argv[1], " ".join(sys.argv[2:]))
