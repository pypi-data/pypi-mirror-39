from typing import Callable
from abc import abstractmethod

class CanvasInterface:

    @abstractmethod
    def register_canvas_click_handler(self, command: Callable):
        raise NotImplementedError()

    @abstractmethod
    def add_line(self, coords_a: tuple, coords_b: tuple):
        raise NotImplementedError()

    @abstractmethod
    def add_rectangle(self, coords_a: tuple, coords_b: tuple):
        raise NotImplementedError()

    @abstractmethod
    def add_circle(self, center: tuple, r: int):
        raise NotImplementedError()

    @abstractmethod
    def canvas_clear(self):
        raise NotImplementedError()

    @abstractmethod
    def set_state_indicator(self, text:str):
        raise NotImplementedError()

    @abstractmethod
    def set_cursor_position_indicator(self, position: tuple):
        raise NotImplementedError()

    @abstractmethod
    def unset_cursor_position_indicator(self):
        raise NotImplementedError()