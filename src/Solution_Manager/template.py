from .manager import SolutionManager
from config_loader import ConfigLoader

cfg = ConfigLoader("config.json").load()

class Template:

    def __init__(self, name_template):
        # load template .josn file
        self.template_cfg = ConfigLoader(f"Code/{name_template}").load()

    def create(self, name, description):
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
        )

if __name__ == "__main__":
    Template("cli_python.json").create("test", "test")