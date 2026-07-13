from .manager import SolutionManager
from .solution import Solution
from config_loader import ConfigLoader
from pathlib import Path
import os
from src.loger import Logger

cfg = ConfigLoader("config.json").load()


class Template:

    def __init__(self, name_template) -> None:
        self.name_template = name_template
        self.template_cfg = ConfigLoader(f"Code/{name_template}").load()

    def create(self, name, description, readme, origin):
        """
        Создание решения
        """

        # шаг 0: подготовка данных
        solution_dir = Path(cfg["SOLUTION_DIR"]) / name / Path(cfg["SRC_DIR"])
        tree = self.template_cfg["TREE"]  # структура решения
        files_list = self.template_cfg.get("FILES", [])
        configuration =  self.template_cfg.get("CONFIGURATION", {})

        # превращаем список [{name, ctx}, ...] в словарь {name: ctx} для быстрого поиска
        files = {item["name"]: item.get("ctx", "") for item in files_list}

        # шаг 1: создание решения
        SolutionManager().create(
            Name=name,
            Description=description,
            Configuration=configuration,
            Script=None,
            Origin=origin
        )

        # шаг 2: создание структуры и файлов из шаблона
        self._build_structure(tree, files, solution_dir)

        # шаг 3: запись readme, если передан явно (перезапишет readme.md из шаблона)
        if readme:
            readme_path = solution_dir / "readme.md"
            os.makedirs(readme_path.parent, exist_ok=True)
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(readme)

        return solution_dir

    def _build_structure(self, tree, files: dict, dest_base: Path):
        """
        Рекурсивно проходит по дереву tree и создаёт
        соответствующую структуру папок/файлов в dest_base,
        беря содержимое файлов из словаря files по имени файла
        """
        os.makedirs(dest_base, exist_ok=True)

        for name, content in tree.items():
            dest_path = dest_base / name

            if content == {}:
                # лист -> файл, ищем содержимое по имени файла
                os.makedirs(dest_path.parent, exist_ok=True)
                code = files.get(name)

                if code is None:
                    open(dest_path, "w", encoding="utf-8").close()
                    Logger().error(
                        f"[WARN](_build_structure) нет содержимого для файла: {name}"
                    )
                else:
                    with open(dest_path, "w", encoding="utf-8") as f:
                        f.write(code)
            else:
                # директория -> создаём и идём вглубь
                os.makedirs(dest_path, exist_ok=True)
                self._build_structure(content, files, dest_path)

    @staticmethod
    def index() -> list[dict]:
        """Индексирует все JSON-шаблоны в папке Code/ и возвращает список объектов."""
        templates = []
        template_dir = Path(cfg["CODE_TEMPLATE_DIR"])

        for path in template_dir.glob("*.json"):
            try:
                data = ConfigLoader(str(path)).load()
                templates.append({
                    "name": data.get("name", path.stem),
                    "description": data.get("description", ""),
                    "file_name": path.name,
                    "language": data.get("CONFIGURATION", {}).get("language", "other"),
                })
            except Exception as e:
                Logger().error(f"[ERROR](index) {path.name}: {e}")
        return templates

    @staticmethod
    def get_code_template(file_name) -> str:
        with open(file_name, "r", encoding="utf-8") as f:
            ctx = f.read()
        return ctx


if __name__ == "__main__":
    Template("my_template_name").create(
        name="test",
        description="test",
        readme="",
        origin=None
    )