from abc import ABC, abstractmethod


class Visitor(ABC):

    def __init__(self, app) -> None:
        self.app = app

    @abstractmethod
    def visit_polyline(self, line):
        raise NotImplementedError

    @abstractmethod
    def visit_rectangle(self, rectangle):
        raise NotImplementedError

    @abstractmethod
    def visit_circle(self, circle):
        raise NotImplementedError
