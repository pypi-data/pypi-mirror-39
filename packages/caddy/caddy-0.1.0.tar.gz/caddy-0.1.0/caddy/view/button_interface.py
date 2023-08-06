from typing import Callable
from enum import Enum
from abc import abstractmethod

class ButtonInterface:

    class ButtonEvents(Enum):
        CURSOR = "cursor"
        MOVE = "move"
        REMOVE = "remove"
        LIST = "list"
        POLYLINE = "polyline"
        RECTANGLE = "rectangle"
        CIRCLE = "circle"

    @abstractmethod
    def register_button_handler(self, button_event: ButtonEvents, command: Callable):
        raise NotImplementedError()
