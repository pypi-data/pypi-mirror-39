from abc import ABC, abstractmethod

from caddy.shared.point import Point


class Shape(ABC):

    @abstractmethod
    def __init__(self, shape_id: int, color: str):
        self.shape_id = shape_id
        self.color = color

    def __repr__(self):
        return self.__str__()

    @abstractmethod
    def move_by(self, point: Point):
        """ Moves the shape relatively by point

        :param point: offset by which the point should be moved
        """
        raise NotImplementedError

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def accept_visitor(self, visitor):
        """ Visits the shape by visitor

        :param visitor: i.e. drawing visitor / printing visitor
        """
        raise NotImplementedError

    @abstractmethod
    def contains_point(self, point: Point) -> bool:
        """ Returns true if the shape overlaps with point

        :param point: test this point for overlapping
        """
        raise NotImplementedError
