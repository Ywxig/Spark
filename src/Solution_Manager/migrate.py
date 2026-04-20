from config_loader import ConfigLoader
from pathlib import Path
from Solution_Manager import SolutionManager
import sys

cfg = ConfigLoader("config.json").load()

def migrate(self, source_dir: str) -> dict:
    source = Path(source_dir)
    if not source.exists():
        print(f"[ERROR] Папка не найдена: {source}")
        sys.exit(1)

    if not source.is_dir():
        print(f"[ERROR] Указанный путь не является папкой: {source}")
        sys.exit(1)

    # Собираем все подпапки — каждая это одно решение
    solution_folders = [p for p in source.iterdir() if p.is_dir()]
    if not solution_folders:
        print(f"[WARN] В папке {source} не найдено ни одного решения.")
        return
    
    print(f"Найдено решений: {len(solution_folders)}")
    print(f"Целевая папка:   {self._root.resolve()}\n")

    migrated = 0
    skipped = 0
    failed = 0

    for folder in sorted(solution_folders):
        name = folder.name
        try:
            # Создаём решение (папку + config.json + src/)
            solution = self.create(Name=name, Description="")
            # Копируем все файлы (рекурсивно) в src/
            SolutionManager._copy_contents(folder, solution.src_path)
            print(f"  [OK]      {name}")
            migrated += 1
        except FileExistsError:
            print(f"  [SKIP]    {name}  (уже существует)")
            skipped += 1
        except Exception as e:
            print(f"  [FAILED]  {name}  ({e})")
            failed += 1

    return {
        "migrated": migrated,
        "skipped": skipped,
        "failed": failed,
    }