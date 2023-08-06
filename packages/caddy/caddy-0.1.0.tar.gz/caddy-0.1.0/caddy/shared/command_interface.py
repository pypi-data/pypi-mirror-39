from abc import abstractmethod

class CommandInterface:

    @abstractmethod
    def add_text_command(self, command: str, command_result:str = ""):
        raise NotImplementedError()

    @abstractmethod
    def add_text_command_result(self, result: str):
        raise NotImplementedError()