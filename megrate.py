"""
Скрипт миграции существующих решений в систему SolutionManager.

Использование:
    python migrate.py <путь к папке с решениями>

Пример:
    python migrate.py C:/Projects/my_solutions
    python migrate.py ../old_solutions

Что делает:
    - Берёт каждую папку из указанной директории
    - Создаёт решение через SolutionManager (Name = имя папки, Description = "")
    - Копирует все файлы из папки в src/ нового решения
    - Пропускает уже существующие решения (не перезаписывает)
"""

import sys
import shutil
from pathlib import Path
from src.loger import Logger

from src.Solution_Manager import SolutionManager


def migrate(source_dir: str) -> None:
    source = Path(source_dir)

    if not source.exists():
        Logger.error(f"[ERROR] Folder not found: {source}")
        sys.exit(1)

    if not source.is_dir():
        Logger.error(f"[ERROR] The specified path is not a folder: {source}")
        sys.exit(1)

    # Собираем все подпапки — каждая это одно решение
    solution_folders = [p for p in source.iterdir() if p.is_dir()]

    if not solution_folders:
        Logger.warn(f"WARN] No solutions were found in the {source} folder.")
        return

    manager = SolutionManager()

    Logger.info(f"[INFO] Count of solutions: {len(solution_folders)}")
    Logger.info(f"[INFO] Target folder:   {manager._root.resolve()}\n")

    migrated = 0
    skipped = 0
    failed = 0

    for folder in sorted(solution_folders):
        name = folder.name

        try:
            # Создаём решение (папку + config.json + src/)
            solution = manager.create(Name=name, Description="")

            # Копируем все файлы (рекурсивно) в src/
            _copy_contents(folder, solution.src_path)

            Logger.info(f"  [OK]      {name}")
            migrated += 1

        except FileExistsError:
            Logger.warn(f"  [SKIP]    {name}  (just exists)")
            skipped += 1

        except Exception as e:
            Logger.error(f"  [FAILED]  {name}  ({e})")
            failed += 1

    Logger.info(f"[INFO] Done. Migrated {migrated} solutions.\n migrated: {migrated}\n skipped: {skipped}\n failed: {failed}")


def _copy_contents(src: Path, dst: Path) -> None:
    """Рекурсивно скопировать содержимое src в dst."""
    for item in src.iterdir():
        target = dst / item.name
        if item.is_dir():
            target.mkdir(exist_ok=True)
            _copy_contents(item, target)
        else:
            shutil.copy2(item, target)


# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         print("Использование: python migrate.py <путь к папке с решениями>")
#         print("Пример:        python migrate.py C:/Projects/my_solutions")
#         sys.exit(1)

#     migrate(sys.argv[1])