from .manager import SolutionManager
from config_loader import ConfigLoader
from pathlib import Path

from src.loger import Logger

cfg = ConfigLoader("config.json").load()

class Template:

    def __init__(self, name_template) -> None:
        # load template .josn file
        self.template_cfg = ConfigLoader(f"Code/{name_template}").load()

    def create(self, name, description, readme):
        """
        Создание решения
        """
        self.template_cfg["Configuration"]["author"] = cfg["AUTHOR"]["NAME"]

        manager = SolutionManager()
        manager.create(
            Name=name,
            Description=description,
            Configuration=self.template_cfg["Configuration"],
            Structure=self.template_cfg["Structure"],
            Script=self.template_cfg["Script"],
            Readme=readme
        )

    @staticmethod
    def index() -> list[dict]:
        """Индексирует все JSON-шаблоны в папке Code/ и возвращает список объектов."""
        templates = []
        for path in Path((cfg["CODE_TEMPLATE_DIR"]).split("/")[0]).glob("*.json"):
            try:
                data = ConfigLoader(str(path)).load()
                templates.append({
                    "name": data.get("name", path.stem),
                    "description": data.get("description", ""),
                    "file_name": path.name,
                })
            except Exception as e:
                Logger().error(f"[ERROR](index) {path.name}: {e}")
        return templates
    @staticmethod
    def get_code_template(file_name) -> str:
        with open(file_name, "r") as f:
            ctx = f.read()
        return ctx
    
Logger().info(f"[INFO] Template module loaded: {Template("cli_python.json").index()}")