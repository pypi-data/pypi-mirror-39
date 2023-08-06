from unittest import TestCase
from unittest.mock import MagicMock

from caddy.model.circle import Circle
from caddy.shared.point import Point


class TestCircle(TestCase):
    def test_move_by(self):
        c = Circle(1, Point(1, 2), 10)
        c.move_by(Point(1, 1))
        self.assertEqual(Point(2, 3), c.center)

    def test_id(self):
        p = Circle(42, Point(1, 1), 1)
        self.assertEqual(42, p.shape_id, 'id matches')

    def test_get_color(self):
        c = Circle(1, Point(1, 2), 10, '#000001')
        self.assertEqual('#000001', c.color, 'color matches',)

    def test_set_color(self):
        c = Circle(1, Point(1, 2), 10, '#000001')
        c.color = '#000002'
        self.assertEqual('#000002', c.color, 'color matches')

    def test_accept_visitor(self):
        c = Circle(1, Point(1, 2), 10, '#000001')
        visitor = MagicMock()
        c.accept_visitor(visitor)
        visitor.visit_circle.assert_called_once_with(c)

    def test___repr__(self):
        c = Circle(1, Point(1, 2), 10, '#000001')
        self.assertEqual('Circle[Center: (1,2), r:10]', c.__str__())

    def test___str__(self):
        c = Circle(1, Point(1, 2), 10, '#000001')
        self.assertEqual('Circle[Center: (1,2), r:10]', c.__str__())

    def test_contains_point(self):
        x = 1
        y = 2
        r = 10  # Must be larger than 4  for the last assert to be correct
        c = Circle(1, Point(1, 2), r, '#000001')
        self.assertTrue(c.contains_point(Point(x, y - r)), 'contains top')
        self.assertTrue(c.contains_point(Point(x, y + r)), 'contains bottom')
        self.assertTrue(c.contains_point(Point(x - r, y)), 'contains left')
        self.assertTrue(c.contains_point(Point(x + r, y)), 'contains right')

        self.assertFalse(c.contains_point(Point(x - r - 1, y)), 'left out of range')
        self.assertFalse(c.contains_point(Point(x + r + 1, y)), 'right out of range')
        self.assertFalse(c.contains_point(Point(x, y - r - 1)), 'top out of range')
        self.assertFalse(c.contains_point(Point(x, y + r + 1)), 'bottom out of range')

        self.assertFalse(c.contains_point(Point(x - r + 1, y - r + 1)), 'top left out of range')
        self.assertFalse(c.contains_point(Point(x + r - 1, y + r - 1)), 'bottom right out of range')
