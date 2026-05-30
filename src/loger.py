import loguru
import sys

from config_loader import ConfigLoader

cfg = ConfigLoader("config.json").load()

class Logger():
    def __init__(self, log_file=cfg["LOG"]["FILE"], level=cfg["LOG"]["LEVEL"], debug=cfg["DEBUG_MODE"]):
        self.logger = loguru.logger
        
        # 1. Сначала удаляем стандартный вывод (если не хотим дублей)
        self.logger.remove()
        
        # 2. Настраиваем вывод в консоль (красивый и цветной)
        self.logger.add(sys.stderr, level=level, colorize=True)
        
        # 3. Настраиваем вывод в файл с ротацией
        self.logger.add(
            log_file, 
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", 
            level=level, 
            rotation="10 MB", # Создаст новый файл, когда этот достигнет 10МБ
            compression="zip" # Старые логи будут архивироваться
        )

    def info(self, message):
        if cfg["DEBUG_MODE"] == True:
            self.logger.info(message)
        else:
            pass

    def error(self, message):
        self.logger.error(message)
    
    def warn(self, message):
        if cfg["DEBUG_MODE"] == True:
            self.logger.warning(message)
        else:
            pass


"""
using:

Logger() = Logger()()
Logger().info("Some info")
Logger().error("Some error")
"""