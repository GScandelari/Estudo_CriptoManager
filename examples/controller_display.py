from src.controller import list_display_lines, parse_display_line
from pprint import pprint

def show_display():
    lines = list_display_lines()
    if not lines:
        print("Display vazio.")
        return
    for line in lines:
        print(line)

if __name__ == "__main__":
    show_display()
