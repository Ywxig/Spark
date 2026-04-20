"""
Entry point программы.
"""

from src.Solution_Manager import Solution, SolutionManager
from config_loader import ConfigLoader

cfg = ConfigLoader("config.json").load()

def main():
    manager = SolutionManager()
    manager.migrate(cfg["MIGRATION_DIR"])

    manager.delete("MyAlgo")

    # Создать новое решение
    sol = manager.create(
        Name="MyAlgo",
        Description="Пример решения",
        Configuration={"language": "python", "version": "1.0"},
    )

    # Добавить исходный файл
    sol.write_source("main.py", 'print("Hello from MyAlgo!")')

    # Изменить конфиг
    sol.set_config("author", "me")

    # Получить список файлов
    print(sol.list_sources())   # ['main.py']

    # Открыть существующее решение позже
    sol2 = manager.get("MyAlgo")
    print(sol2.Name)            # MyAlgo
    print(sol2.Configuration)   # {'language': 'python', 'version': '1.0', 'author': 'me'}

    # Индексировать все решения
    all_solutions = manager.index()
    print(all_solutions)


if __name__ == "__main__":
    main()