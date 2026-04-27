import os
from pathlib import Path
from .manager import SolutionManager
from config_loader import ConfigLoader
import shutil

from ..loger import Logger

cfg = ConfigLoader("config.json").load()

import sys

class Migration:
    """Класс, представляющий одну конкретную миграцию (директорию)"""
    def __init__(self, path: Path):
        self.path = path
        self.name = path.name

    def __repr__(self):
        return f"<Migration: {self.name}>"


class Migrations:
    def __init__(self, source_dir: str = None):
        # Если путь не передан, берем из конфига
        path_str = source_dir or cfg.get("MIGRATION_DIR")
        if not path_str:
            raise ValueError("MIGRATION_DIR не указан в конфигурации или аргументах")
            
        self.source_dir = Path(path_str)
        self.manager = SolutionManager()

    def list_migrations(self) -> list[str]:
        """Возвращает отсортированный список имен папок-миграций"""
        if not self.source_dir.exists():
            return []
        
        # Сортировка важна для последовательного применения миграций
        dirs = [
            d.name for d in self.source_dir.iterdir() 
            if d.is_dir() and not d.name.startswith('.')
        ]
        return sorted(dirs)

    def index(self) -> list[Migration]:
        """
        Сканирует директорию и возвращает список объектов Migration.
        Это и есть ваш список директорий для миграции, обернутый в объекты.
        """
        return [Migration(self.source_dir / name) for name in self.list_migrations()]

    def run_all(self):
        """Метод для запуска процесса миграции на основе проиндексированных данных"""
        results = {"migrated": 0, "skipped": 0, "failed": 0}
        
        migrations = self.index()
        
        for m in migrations:
            try:
                # Используем вашу логику из функции migrate
                solution = self.manager.create(Name=m.name, Description="")
                # Проверяем, что create вернул объект, а не None
                if solution is None:
                    raise ValueError(f"manager.create вернул None для '{m.name}'")
                Migrations._copy_contents(m.path, solution.src_path)
                results["migrated"] += 1
            except FileExistsError:
                results["skipped"] += 1
            except Exception:
                results["failed"] += 1
                
        return results
    @staticmethod
    def migrate(source_dir: str) -> None:
        source = Path(source_dir)

        if not source.exists():
            Logger().error(f"[ERROR] Folder not found: {source}")
            sys.exit(1)

        if not source.is_dir():
            Logger().error(f"[ERROR] The specified path is not a folder: {source}")
            sys.exit(1)

        # Собираем все подпапки — каждая это одно решение
        solution_folders = [p for p in source.iterdir() if p.is_dir()]

        if not solution_folders:
            Logger().warn(f"WARN] No solutions were found in the {source} folder.")
            return

        manager = SolutionManager()

        Logger().info(f"[INFO] Count of solutions: {len(solution_folders)}")
        Logger().info(f"[INFO] Target folder:   {manager._root.resolve()}\n")

        migrated = 0
        skipped = 0
        failed = 0

        for folder in sorted(solution_folders):
            name = folder.name

            try:
                # Создаём решение (папку + config.json + src/)
                solution = manager.create(Name=name, Description="", Configuration=cfg["MIGRATION"]["Configuration"], Readme="")

                # Проверяем, что create вернул объект, а не None
                if solution is None:
                    raise ValueError("manager.create вернул None")

                # Копируем все файлы (рекурсивно) в src/
                Migrations._copy_contents(folder, solution.src_path)
                # Create a readme.md
                solution.write_source("readme.md", "")

                Logger().info(f"  [OK]      {name}")
                migrated += 1

            except FileExistsError:
                Logger().warn(f"  [SKIP]    {name}  (just exists)")
                skipped += 1

            except Exception as e:
                Logger().error(f"  [FAILED]  {name}  ({e})")
                failed += 1

        Logger().info(f"[INFO] Done. Migrated {migrated} solutions.\n migrated: {migrated}\n skipped: {skipped}\n failed: {failed}")

    @staticmethod
    def _copy_contents(src: Path, dst: Path) -> None:
        """Рекурсивно скопировать содержимое src в dst."""
        for item in src.iterdir():
            target = dst / item.name
            if item.is_dir():
                target.mkdir(exist_ok=True)
                Migrations._copy_contents(item, target)
            else:
                shutil.copy2(item, target)