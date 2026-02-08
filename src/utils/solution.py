import os
import shutil
import json
from datetime import datetime
from pathlib import Path
from colorama import Fore

class Solution():

    def __init__(self, name_):
        self.name_ = name_
        self.locate_ = f"Solutions/{name_}"

    def _load_config(self):
        pass

    def tree(self, indent=0):
        path = Path(self.locate_)
        
        # Проходим по всем элементам в директории
        # Сортируем, чтобы сначала шли папки, а потом файлы (для красоты)
        items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
        
        for item in items:
            # Рисуем отступ
            prefix = "    " * indent + ("└── " if not item.is_dir() else "📁 ")
            print(f"{prefix}{item.name}")
            
            # Если это директория, заходим внутрь (рекурсия)
            if item.is_dir():
                self.tree(item, indent + 1)


    def new(self):
        os.makedirs(self.locate_, exist_ok=True)
        solution_config = {
            "SOLUTION_NAME" : self.name_,
            "DATE" : str(datetime.now()),
            "FILES" : []
        }
        with open(f"{self.locate_}/.config.json", 'w', encoding='utf-8') as f:
            json.dump(solution_config, f, ensure_ascii=False, indent=4)
            f.close()


    def mkdir(self, dir_name) -> None:
        try:
            os.mkdir(f"{self.locate_}/{dir_name}")
        except FileExistsError:
            pass

    def mkfile(self, file_name) -> None:
        open(f"{self.locate_}/{file_name}", "w", encoding="utf-8").write("")

    def remove(self) -> None:
        shutil.rmtree(self.locate_)

    def pwd(self):
        path = self.locate_
        if os.path.isdir(path):
            return self.locate_
        else:
            return None
        
    def ls(path):
        ls_list = []
        path = Path(f"{path}")
        for item in path.iterdir():
            if item.is_file():
                ls_list.append(f"{Fore.WHITE} {str(item.name)} {Fore.RESET}")
            elif item.is_dir():
                ls_list.append(f"{Fore.CYAN} {str(item.name)} {Fore.RESET}")
        print("".join(ls_list)) 
