import json
from pathlib import Path
from typing import Any
from config_loader import ConfigLoader

import sys

cfg = ConfigLoader("config.json").load()

class Solution:
    """
    Представляет одно решение, привязанное к папке на диске.
    Создаётся только через SolutionManager.create().

    Структура папки:
        Solutions/<Name>/
        ├── config.json   — Name, Description, Configuration
        └── src/          — исходный код решения
    """

    CONFIG_FILE = cfg["CONFIG_FILE"]
    SRC_DIR = cfg["SRC_DIR"]

    def __init__(self, path: Path) -> None:
        self._path = path
        self._config_path = path / self.CONFIG_FILE
        self._src_path = path / self.SRC_DIR

        if not self._config_path.exists():
            raise FileNotFoundError(
                f"config.json не найден в {path}. "
                "Используйте SolutionManager.create() для создания решения."
            )

        self._data = self._load_config()

    
    # Свойства — при изменении сразу сохраняются на диск
    

    @property
    def Name(self) -> str:
        return self._data["Name"]

    @Name.setter
    def Name(self, value: str) -> None:
        self._data["Name"] = value
        self._save_config()

    @property
    def Description(self) -> str:
        return self._data["Description"]

    @Description.setter
    def Description(self, value: str) -> None:
        self._data["Description"] = value
        self._save_config()

    @property
    def Configuration(self) -> dict:
        return self._data["Configuration"]

    @Configuration.setter
    def Configuration(self, value: dict) -> None:
        self._data["Configuration"] = value
        self._save_config()

    @property
    def path(self) -> Path:
        """Корневая папка решения."""
        return self._path

    @property
    def src_path(self) -> Path:
        """Папка с исходным кодом."""
        return self._src_path

    
    # Работа с Configuration
    

    def get_config(self, key: str, default: Any = None) -> Any:
        """Получить значение из Configuration по ключу."""
        return self._data["Configuration"].get(key, default)

    def set_config(self, key: str, value: Any) -> None:
        """Установить значение в Configuration и сохранить на диск."""
        self._data["Configuration"][key] = value
        self._save_config()

    def remove_config_key(self, key: str) -> bool:
        """Удалить ключ из Configuration. Вернуть True если ключ существовал."""
        existed = key in self._data["Configuration"]
        self._data["Configuration"].pop(key, None)
        if existed:
            self._save_config()
        return existed

    def reload(self) -> None:
        """Перечитать config.json с диска (если файл изменён снаружи)."""
        self._data = self._load_config()

    
    # Работа с исходным кодом (src/)
    

    def list_sources(self) -> list[str]:
        """Вернуть список файлов в src/."""
        return [f.name for f in self._src_path.iterdir() if f.is_file()]

    def read_source(self, filename: str) -> str:
        """Прочитать файл из src/."""
        file = self._src_path / filename
        if not file.exists():
            raise FileNotFoundError(f"Файл {filename!r} не найден в src/.")
        return file.read_text(encoding="utf-8")

    def write_source(self, filename: str, content: str) -> None:
        """Записать (создать/перезаписать) файл в src/."""
        (self._src_path / filename).write_text(content, encoding="utf-8")

    def delete_source(self, filename: str) -> None:
        """Удалить файл из src/."""
        file = self._src_path / filename
        if not file.exists():
            raise FileNotFoundError(f"Файл {filename!r} не найден в src/.")
        file.unlink()

    def source_path(self, filename: str) -> Path:
        """Вернуть полный путь к файлу в src/."""
        return self._src_path / filename

    
    # Приватные методы
    

    def _load_config(self) -> dict:
        with open(self._config_path, encoding="utf-8") as f:
            return json.load(f)

    def _save_config(self) -> None:
        with open(self._config_path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=4)

    def __repr__(self) -> str:
        return f"Solution(Name={self.Name!r}, path={str(self._path)!r})"