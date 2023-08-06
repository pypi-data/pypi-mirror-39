from caddy.model.circle import Circle
from caddy.model.polyline import PolyLine
from caddy.model.rectangle import Rectangle
from caddy.presenter.visitor.visitor import Visitor
from caddy.shared.point import Point


class DrawingVisitor(Visitor):

    def visit_polyline(self, line: PolyLine):
        prev_point = line.points[0]
        for next_point in line.points[1:]:
            self.app.canvas.add_line(prev_point, next_point)
            prev_point = next_point

    def visit_rectangle(self, rectangle: Rectangle):
        offset = Point(1, 1)
        self.app.canvas.add_rectangle(tuple(rectangle.top_left_corner),
                                      tuple(rectangle.bottom_right_corner + offset))

    def visit_circle(self, circle: Circle):
        self.app.canvas.add_circle(tuple(circle.center), circle.radius)
