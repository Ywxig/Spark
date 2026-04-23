# SolutionManager

import json
from .solution import Solution
from config_loader import ConfigLoader
import shutil
from pathlib import Path

cfg = ConfigLoader("config.json").load()


class SolutionManager:
    """
    Управляет окружением решений: создаёт/удаляет папки,
    индексирует существующие решения.
    Вся работа с содержимым — через объект Solution.
    """

    SOLUTIONS_DIR = cfg["SOLUTION_DIR"]

    def __init__(self) -> None:
        self._root = Path(self.SOLUTIONS_DIR)
        self._root.mkdir(exist_ok=True)

    def create(
        self,
        Name: str,
        Description: str,
        Configuration: dict | None = None,
        Structure: list[dict] | None = None,
    ) -> Solution:
        """
        Создать окружение для нового решения и вернуть объект Solution.

        Raises:
            FileExistsError: если решение с таким именем уже существует.
        """
        solution_path = self._root / Name

        if solution_path.exists():
            raise FileExistsError(f"Решение {Name!r} уже существует.")

        solution_path.mkdir(parents=True)
        (solution_path / Solution.SRC_DIR).mkdir()

        config_data = {
            "Name": Name,
            "Description": Description,
            "Configuration": Configuration or {},
        }
        with open(solution_path / Solution.CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config_data, f, ensure_ascii=False, indent=4)

        # create files using templates

        for item in Structure:
            with open(solution_path / Solution.SRC_DIR / item["name"], "w", encoding="utf-8") as f:
                f.write(item["ctx"])

        return Solution(solution_path)

    def delete(self, Name: str) -> None:
        """Удалить папку решения целиком."""
        solution_path = self._root / Name
        if not solution_path.exists():
            raise FileNotFoundError(f"Решение {Name!r} не найдено.")
        shutil.rmtree(solution_path)

    def get(self, Name: str) -> Solution:
        """Получить объект Solution для уже существующего решения."""
        solution_path = self._root / Name
        if not solution_path.exists():
            raise FileNotFoundError(f"Решение {Name!r} не найдено.")
        return Solution(solution_path)

    def list_solutions(self) -> list[str]:
        """Вернуть список имён всех существующих решений."""
        return [
            d.name for d in self._root.iterdir()
            if d.is_dir() and (d / Solution.CONFIG_FILE).exists()
        ]

    def index(self) -> list[Solution]:
        """Проиндексировать все решения. Вернуть список объектов Solution."""
        return [Solution(self._root / name) for name in self.list_solutions()]

    def __repr__(self) -> str:
        return f"SolutionManager(root={str(self._root)!r})"
    
    @staticmethod
    def _copy_contents(src: Path, dst: Path) -> None:
        """Рекурсивно скопировать содержимое src в dst."""
        for item in src.iterdir():
            target = dst / item.name
            if item.is_dir():
                target.mkdir(exist_ok=True)
                SolutionManager._copy_contents(item, target)
            else:
                shutil.copy2(item, target)

if __name__ == "__main__":
    manager = SolutionManager()
    #testing
    manager.create("test")
    manager.delete("test")
