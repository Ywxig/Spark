# cli/__init__.py
# Import the command_handler module to make it accessible
from . import command_handler

# Optionally expose the module at package level
__all__ = ['command_handler']