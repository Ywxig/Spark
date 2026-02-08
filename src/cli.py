import os
from pathlib import Path
from utils import solution
from colorama import Fore

class CLI:
    def __init__(self, invte_, CONFIG):
        self.type_ = CONFIG["type_default_"]
        self.invte_ = invte_
        self.run_ = True
        self.type_color_ = Fore.GREEN
        self.type_invite_color_ = Fore.LIGHTMAGENTA_EX
        self.current_solution = None 
        self.CONFIG = CONFIG

        # Регистрация команд
        self.commands = {
            "help": self.CMD.help,
            "new" : self.CMD.new,
            "hover": self.CMD.hover,
            "file": self.CMD.add_file,
            "pwd" : self.CMD.pwd,
            "remove" : self.CMD.remove,
            "rm" : self.CMD.remove,
            "ls" : self.CMD.ls,
            "exit": self.cmd_exit,
        }

    class CMD:
        """
        Везде добавляем CONFIG в аргументы. 
        Даже если он не используется сейчас, это сохранит структуру.
        """
        @staticmethod
        def help(ctx, CONFIG, args):
            print(CONFIG["help"]["hover"])
            
        @staticmethod
        def hover(ctx, CONFIG, args): # Добавлен CONFIG
            if not args:
                print("Error: give name of solution.")
                print(CONFIG["help"]["hover"])
                return
            
            project_name = args[0]
            if not Path(f"Solutions/{project_name}").is_dir():
                print(f"Error: Solution '{project_name}' not found.")
                return

            ctx.current_solution = solution.Solution(project_name)
            ctx.change_type(project_name)

        @staticmethod
        def add_file(ctx, CONFIG, args):
            if not args:
                print("Error: give file name.")
                print(CONFIG["help"]["file"])
                return
                
            if ctx.current_solution:
                ctx.current_solution.mkfile(args[0])
            else:
                print("Error: No project hovered!")

        @staticmethod
        def new(ctx, CONFIG, args):
            if not args:
                print("Error: give name of solution.")
                print(CONFIG["help"]["new"])
                return
            ctx.current_solution = solution.Solution(args[0])
            ctx.change_type(args[0])
            ctx.current_solution.new()

        @staticmethod
        def remove(ctx, CONFIG, args):
            if not args:
                print("Error: give name of solution.")
                print(CONFIG["help"]["remove"])
                return
            
            # Логика удаления
            if args[0] == "-s":
                if ctx.current_solution:
                    ctx.current_solution.remove()
                else:
                    print("Error: Nothing to remove (-s).")
            else:
                rem_sol = solution.Solution(args[0])
                rem_sol.remove()
                if ctx.get_type() == args[0]:
                    ctx.current_solution = None
                    ctx.change_type(CONFIG["type_default_"])

        @staticmethod
        def ls(ctx, CONFIG, args):
            if args and (args[0] == "-h" or args[0] == "-help"):
                print(CONFIG["help"]["ls"])
                return

            if not args:
                solution.Solution.ls("Solutions")
            elif args[0] == "-s":
                if ctx.type_ == CONFIG["type_default_"]:
                    solution.Solution.ls("Solutions")
                else:
                    ctx.current_solution.tree()
            else:
                solution.Solution.ls(f"Solutions/{args[0]}")
                            
        @staticmethod
        def pwd(ctx, CONFIG, args):
            if args and (args[0] == "-h" or args[0] == "-help"):
                print(CONFIG["help"]["pwd"])
                return

            if ctx.get_type() == "~":
                print(os.getcwd())
            elif args and args[0] == "-s":
                print(f"{os.getcwd()}/{ctx.get_type()}")
            else:
                print(os.getcwd())

    def change_type(self, new_type):
        self.type_ = new_type

    def get_type(self):
        return self.type_

    def cmd_exit(self, ctx, CONFIG, args): # Добавлен CONFIG для совместимости
        self.run_ = False

    def run(self):
        while self.run_:
            try:
                prompt = f"({self.type_color_}{self.type_}{Fore.RESET}) {self.type_invite_color_}{self.invte_}{Fore.RESET}"
                user_input = input(prompt).strip()
                if not user_input: continue

                parts = user_input.split()
                cmd_name = parts[0].lower()
                args = parts[1:]

                if cmd_name in self.commands:
                    # КЛЮЧЕВОЕ ИЗМЕНЕНИЕ: передаем self.CONFIG третьим аргументом
                    self.commands[cmd_name](self, self.CONFIG, args)
                else:
                    print(f"Unknown command: {cmd_name}")
            except KeyboardInterrupt:
                self.cmd_exit(self, self.CONFIG, [])
            except Exception as e:
                print(f"An error occurred: {e}")