from abc import ABC, abstractmethod
from typing import Sequence, List

from caddy.model.shape import Shape
from caddy.shared.point import Point


class ModelObserver(ABC):
    @abstractmethod
    def on_model_changed(self):
        raise NotImplementedError()


class ModelInterface(ABC):
    @abstractmethod
    def attach_observer(self, observer: ModelObserver):
        raise NotImplementedError()

    @abstractmethod
    def detach_observer(self, observer: ModelObserver):
        raise NotImplementedError()

    @abstractmethod
    def add_circle(self, center: Point, radius: int, color: str = '#000000') -> int:
        raise NotImplementedError()

    @abstractmethod
    def add_rectangle(self, top_left_corner: Point, bottom_right_corner: Point, color: str = '#000000') -> int:
        raise NotImplementedError()

    @abstractmethod
    def add_polyline(self, points: Sequence[Point], color: str = '#000000'):
        raise NotImplementedError()

    @abstractmethod
    def remove_overlapping_with(self, point: Point):
        raise NotImplementedError()

    @abstractmethod
    def overlapping_with(self, point: Point) -> List[Shape]:
        raise NotImplementedError()

    @abstractmethod
    def find_by_id(self, shape_id: int):
        raise NotImplementedError()

    @abstractmethod
    def clear(self):
        raise NotImplementedError()

    @abstractmethod
    def move_by(self, overlapping: Point, offset: Point):
        raise NotImplementedError()

    @abstractmethod
    def accept_visitor(self, visitor):
        raise NotImplementedError()
