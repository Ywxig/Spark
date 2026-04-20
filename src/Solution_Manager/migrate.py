from pathlib import Path
from .Solution import SolutionManager
import sys

def migrate(manager: SolutionManager, source_dir: str) -> dict:
    source = Path(source_dir)

    if not source.exists() or not source.is_dir():
        raise ValueError(f"Папка не найдена или не является директорией: {source}")

    solution_folders = [p for p in source.iterdir() if p.is_dir()]
    if not solution_folders:
        return {"migrated": 0, "skipped": 0, "failed": 0}

    migrated = skipped = failed = 0

    for folder in sorted(solution_folders):
        try:
            solution = manager.create(Name=folder.name, Description="")
            SolutionManager._copy_contents(folder, solution.src_path)
            migrated += 1
        except FileExistsError:
            skipped += 1
        except Exception:
            failed += 1

    return {"migrated": migrated, "skipped": skipped, "failed": failed}