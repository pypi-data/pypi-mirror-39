from typing import Callable
from abc import abstractmethod
from caddy.shared.command_interface import CommandInterface

class CLIInterface(CommandInterface):

    @abstractmethod
    def register_entry_handler(self, command: Callable):
        raise NotImplementedError()

    @abstractmethod
    def cli_clear(self):
        raise NotImplementedError()