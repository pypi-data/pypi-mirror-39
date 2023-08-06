from caddy.model.shape import Shape
from caddy.shared.point import Point


class Rectangle(Shape):

    def __init__(self, shape_id: int, point1: Point, point2: Point, color='#000000'):
        super().__init__(shape_id, color)

        self.top_left_corner: Point = Point(min(point1.x, point2.x), max(point1.y, point2.y))
        self.bottom_right_corner: Point = Point(max(point1.x, point2.x), min(point1.y, point2.y))

    def move_by(self, p: Point):
        self.top_left_corner += p
        self.bottom_right_corner += p

    def __str__(self) -> str:
        return 'Rectangle[Top left corner: ' + str(self.top_left_corner) + ', Bottom right corner: ' \
               + str(self.bottom_right_corner) + ']'

    def accept_visitor(self, visitor):
        visitor.visit_rectangle(self)

    def contains_point(self, p: Point) -> bool:
        return self.bottom_right_corner.x >= p.x >= self.top_left_corner.x and \
               self.top_left_corner.y >= p.y >= self.bottom_right_corner.y
