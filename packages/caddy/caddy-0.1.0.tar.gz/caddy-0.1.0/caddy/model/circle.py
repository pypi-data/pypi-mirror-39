from caddy.model.shape import Shape
from caddy.shared.point import Point


class Circle(Shape):

    def __init__(self, shape_id: int, center: Point, radius: int, color='#000000'):
        super().__init__(shape_id, color)
        self.center: Point = center
        self.radius: int = radius

    def move_by(self, point: Point):
        self.center += point

    def __str__(self) -> str:
        return 'Circle[Center: ' + str(self.center) + ', r:' \
               + str(self.radius) + ']'

    def accept_visitor(self, visitor):
        visitor.visit_circle(self)

    def contains_point(self, point: Point) -> bool:
        return self.center.dist_from(point) <= self.radius
