from math import floor
from typing import Sequence

from caddy.model.shape import Shape
from caddy.shared.point import Point


class PolyLine(Shape):
    TOLERANCE = 5

    def __init__(self, shape_id: int, points: Sequence[Point], color='#000000'):
        super().__init__(shape_id, color)
        self.points: Sequence[Point] = points  # points -> collection of joints (+ first and last point)

    def move_by(self, point: Point):
        """
        Move all points in polyline by offset
        :param point: offset
        """
        self.points = list(map(lambda p: p + point, self.points))

    def __str__(self) -> str:
        return 'PolyLine[Points: ' + str(self.points) + ']'

    def accept_visitor(self, visitor):
        visitor.visit_polyline(self)

    def contains_point(self, p: Point) -> bool:
        """
        Got this from https://stackoverflow.com/a/1501725


                         p
                       + |+
                     +   | +
                   +    d|  +
                 +       |   +
                u--------P----v

        P: projection of point p on line segment uv
        t: number between [0,1] expressing the ratio of:
            distance of P from u / length of |uv|

        """

        if len(self.points) == 0:
            return False

        v = self.points[0]
        for w in self.points[1:]:

            l2 = Point.dist_squared(v, w)  # |u - v|^2
            if l2 == 0:
                dist = p.dist_from(v)
            else:
                t = ((p.x - v.x) * (w.x - v.x) + (p.y - v.y) * (w.y - v.y)) / l2
                t = max(0., min(1., t))
                projection = Point(floor(v.x + t * (w.x - v.x)), floor(v.y + t * (w.y - v.y)))
                dist = p.dist_from(projection)

            if dist <= self.TOLERANCE:
                return True

            v = w

        return False
