from math import hypot, floor


class Point:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __iter__(self):
        yield self.x
        yield self.y

    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Point') -> 'Point':
        return Point(self.x - other.x, self.y - other.y)

    def __iadd__(self, other: 'Point'):
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other: 'Point'):
        self.x -= other.x
        self.y -= other.y
        return self

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '(' + str(self.x) + ',' + str(self.y) + ')'

    def __eq__(self, other: 'Point') -> bool:
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self == other

    def as_tuple(self) -> tuple:
        return self.x, self.y

    def dist_from(self, p: 'Point') -> float:
        return hypot(self.x - p.x, self.y - p.y)

    @staticmethod
    def dist_from_squared(self, p2: 'Point') -> float:
        return (self.x - p2.x) ** 2 + (self.y - p2.y) ** 2

    @staticmethod
    def dist(p1: 'Point', p2: 'Point') -> float:
        return hypot(p1.x - p2.x, p1.y - p2.y)

    @staticmethod
    def dist_squared(p1: 'Point', p2: 'Point') -> float:
        return (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2

    @staticmethod
    def midpoint(p1: 'Point', p2: 'Point') -> 'Point':
        """
        Uses the midpoint formula (x_m,y_m) = ((x1 + x2)/2, (y1 + y2)/2)
        Used floor from math library to round the number down to the closest integer
        :param p1: first point
        :param p2: second point
        :return: the point in the middle between p1 and p2
        """
        return Point(floor((p1.x + p2.x) / 2), floor((p1.y + p2.y) / 2))
