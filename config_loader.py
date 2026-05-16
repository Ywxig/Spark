import json


class ConfigLoader:

    def __init__(self, Config_File_Path: str):
        self.Config_File_Path = Config_File_Path

    def load(self) -> dict:
        """Загрузить конфигурацию из файла."""
        with open(self.Config_File_Path, "r", encoding="utf-8") as f:
            return json.load(f)
        
    def set(self, field, value):
        """Изменить поле в конфигурации."""
        with open(self.Config_File_Path, "r", encoding="utf-8") as f:
            return json.load(f)
        
    def save(self, data: dict) -> None:
        with open(self.Config_File_Path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)