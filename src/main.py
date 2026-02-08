import sys
import os
from cli import CLI
import json

def main():
    with open('config.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Создаем экземпляр класса
    cli = CLI(data["invite_"], data)
    cli.run()

if __name__ == "__main__":
    main()