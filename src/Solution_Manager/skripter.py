import os
import sys

import subprocess

from loger import Logger

"""
this module using for setup the project
like .venv and install the dependencies
"""

class Script:

    def __init__(self, working_dir):
        self.working_dir = working_dir
    
        def execute(self, command : list):
            """
            Execute a list of shell commands sequentially in the working directory.
            
            Args:
                command (list): A list of shell command strings to be executed.
                               Empty or whitespace-only commands will be skipped.
            
            Raises:
                RuntimeError: If any command fails (returns non-zero exit code).
                             The error message includes the exit code and the failed command.
            """
    
            for cmd in command:
                cmd = cmd.strip()
                if not cmd:
                    continue
                
                result = subprocess.run(cmd, shell=True, check=False)
                if result.returncode != 0:
                    Logger.error(f"Command failed with exit code {result.returncode}: {cmd}")
                    raise RuntimeError(f"Command failed with exit code {result.returncode}: {cmd}")
        