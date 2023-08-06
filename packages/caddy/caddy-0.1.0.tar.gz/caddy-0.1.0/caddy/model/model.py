from typing import Sequence, List

from caddy.model.circle import Circle
from caddy.model.model_interface import ModelObserver, ModelInterface
from caddy.model.polyline import PolyLine
from caddy.model.rectangle import Rectangle
from caddy.model.shape import Shape
from caddy.shared.point import Point


class IdGenerator:
    def __init__(self, offset: int = 0):
        self.id: int = offset

    def next(self) -> int:
        self.id += 1
        return self.id


class Model(ModelInterface):
    def __init__(self):
        self.shapes: List[Shape] = []
        self._observers: List[ModelObserver] = []
        self._id_gen = IdGenerator()

    def attach_observer(self, observer: ModelObserver):
        self._observers.append(observer)

    def detach_observer(self, observer: ModelObserver):
        self._observers = [o for o in self._observers if o != observer]

    def add_circle(self, center: Point, radius: int, color: str = '#000000') -> int:
        shape_id: int = self._id_gen.next()
        self.shapes.append(Circle(shape_id, center, radius, color))
        self._update()
        return shape_id

    def add_rectangle(self, top_left_corner: Point, bottom_right_corner, color: str = '#000000') -> int:
        shape_id: int = self._id_gen.next()
        self.shapes.append(Rectangle(shape_id, top_left_corner, bottom_right_corner, color))
        self._update()
        return shape_id

    def add_polyline(self, points: Sequence[Point], color: str = '#000000'):
        shape_id: int = self._id_gen.next()
        self.shapes.append(PolyLine(shape_id, points, color))
        self._update()
        return shape_id

    def remove_overlapping_with(self, point: Point):
        orig_len = len(self.shapes)
        self.shapes = [s for s in self.shapes if not s.contains_point(point)]
        orig_len != len(self.shapes) and self._update()

    def overlapping_with(self, point: Point) -> List[Shape]:
        return [s for s in self.shapes if s.contains_point(point)]

    def find_by_id(self, shape_id: int):
        lst = [s for s in self.shapes if s.shape_id == shape_id]
        return lst[0] if len(lst) else None

    def clear(self):
        self.shapes = []
        self._update()

    def move_by(self, overlapping: Point, offset: Point):
        for shape in self.overlapping_with(overlapping):
            shape.move_by(offset)
        len(self.shapes) and self._update()

    def accept_visitor(self, visitor):
        for shape in self.shapes:
            shape.accept_visitor(visitor)

    def _update(self):
        for o in self._observers:
            o.on_model_changed()

    def remove_by_id(self, shape_id):
        if shape_id < 0:
            return

        orig_len = len(self.shapes)
        self.shapes = [s for s in self.shapes if s.shape_id != shape_id]
        orig_len != len(self.shapes) and self._update()
