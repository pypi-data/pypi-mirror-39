from unittest import TestCase
from unittest.mock import MagicMock

from caddy.model.rectangle import Rectangle
from caddy.shared.point import Point


class TestRectangle(TestCase):
    def test_init(self):
        def assert_points(r: Rectangle):
            self.assertEqual(Point(1, 2), r.top_left_corner)
            self.assertEqual(Point(2, 1), r.bottom_right_corner)

        r = Rectangle(0, Point(1, 1), Point(2,2))
        assert_points(r)

        r = Rectangle(0, Point(1, 2), Point(2, 1))
        assert_points(r)

        r = Rectangle(0, Point(2, 1), Point(1, 2))
        assert_points(r)

        r = Rectangle(0, Point(2, 2), Point(1, 1))
        assert_points(r)

    def test_move_by(self):
        r = Rectangle(1, Point(1, 2), Point(2, 2))
        r.move_by(Point(1, 1))
        self.assertEqual(Point(2, 3), r.top_left_corner)
        self.assertEqual(Point(3, 3), r.bottom_right_corner)

    def test_id(self):
        p = Rectangle(42, Point(1, 1), Point(2, 1))
        self.assertEqual(42, p.shape_id, 'id matches')

    def test_get_color(self):
        r = Rectangle(1, Point(1, 2), Point(2, 1), '#000001')
        self.assertEqual('#000001', r.color, 'color matches')

    def test_set_color(self):
        r = Rectangle(1, Point(1, 2), Point(2, 1), '#000001')
        r.color = '#000002'
        self.assertEqual('#000002', r.color, 'color matches')

    def test_accept_visitor(self):
        r = Rectangle(1, Point(1, 2), Point(2, 1), '#000001')
        visitor = MagicMock()
        r.accept_visitor(visitor)
        visitor.visit_rectangle.assert_called_once_with(r)

    def test___repr__(self):
        r = Rectangle(1, Point(1, 2), Point(2, 1), '#000001')
        self.assertEqual('Rectangle[Top left corner: (1,2), Bottom right corner: (2,1)]', r.__str__())

    def test___str__(self):
        r = Rectangle(1, Point(1, 2), Point(2, 1), '#000001')
        self.assertEqual('Rectangle[Top left corner: (1,2), Bottom right corner: (2,1)]', r.__str__())

    def test_contains_point(self):
        x = 1
        y = 2
        w = 10
        h = 10
        r = Rectangle(1, Point(x, y), Point(x + w, y - h), '#000001')
        self.assertTrue(r.contains_point(Point(x, y)), 'contains top left')
        self.assertTrue(r.contains_point(Point(x + w, y)), 'contains top right')
        self.assertTrue(r.contains_point(Point(x, y - h)), 'contains bottom left')
        self.assertTrue(r.contains_point(Point(x + w, y - h)), 'contains bottom right')
        self.assertFalse(r.contains_point(Point(x - 1, y)), 'left out of range')
        self.assertFalse(r.contains_point(Point(x + w + 1, y)), 'right out of range')
        self.assertFalse(r.contains_point(Point(x, y + 1)), 'top out of range')
        self.assertFalse(r.contains_point(Point(x, y - h - 1)), 'bottom out of range')
