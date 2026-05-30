import subprocess
import os

from src.loger import Logger

class CommandExecutor:
    def __init__(self, working_dir):
        # Проверяем, существует ли директория сразу
        if not os.path.exists(working_dir):
            raise FileNotFoundError(f"Директория не найдена: {working_dir}")
        
        self.working_dir = working_dir
        self.logger = Logger() # Предполагаем, что Logger настроен

    def execute(self, commands: list):
        """
        Выполняет список shell-команд в заданной директории.
        """
        for cmd in commands:
            cmd = cmd.strip()
            if not cmd:
                continue

            self.logger.info(f"Запуск команды: '{cmd}' в директории: {self.working_dir}")

            try:
                # Используем параметр cwd вместо os.chdir
                result = subprocess.run(
                    cmd,
                    shell=True,
                    cwd=self.working_dir, # <-- Вот здесь магия
                    text=True,
                    capture_output=True # Чтобы получить текст ошибки
                )

                if result.returncode != 0:
                    error_details = result.stderr.strip() or "Нет вывода ошибки"
                    log_msg = f"Ошибка команды (код {result.returncode}): {cmd} | Детали: {error_details}"
                    
                    self.logger.error(log_msg)
                    raise RuntimeError(log_msg)

                self.logger.info(f"Успешно выполнено: {cmd}")

            except Exception as e:
                self.logger.error(f"Системная ошибка при выполнении '{cmd}': {e}")
                raise