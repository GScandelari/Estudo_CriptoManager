import sys
from src.controller import list_display_lines, try_decrypt_line_for_sender

def machine_read(sender_id: str):
    lines = list_display_lines()
    if not lines:
        print("Display vazio.")
        return

    for line in lines:
        status, content = try_decrypt_line_for_sender(line, sender_id)
        if status == "ok":
            print(f"{sender_id} -> DESCRIPTOGRAFADO: {content}")
        elif status == "no-key":
            print(f"{sender_id} -> Sem chave local para esta mensagem (permanece criptografada): {line}")
        elif status == "invalid-key":
            print(f"{sender_id} -> Chave local inválida para esta mensagem.")
        elif status == "encrypted":
            print(f"{sender_id} -> Mensagem criptografada (não consegue descriptografar): {line}")
        # ignoramos linhas de outros remetentes
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python machine_reader.py <SENDER_ID>")
    else:
        machine_read(sys.argv[1])
