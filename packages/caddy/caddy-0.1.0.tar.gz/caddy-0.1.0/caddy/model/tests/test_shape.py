from unittest import TestCase
from unittest.mock import patch, Mock

from caddy.model.shape import Shape
from caddy.shared.point import Point


class TestShape(TestCase):

    def test_cannot_instantiate(self):
        with self.assertRaises(TypeError):
            Shape(1, '#000000')

    @patch.multiple(Shape, __abstractmethods__=set())
    def test_get_color(self):
        s = Shape(1, '#000001')
        self.assertEqual('#000001', s.color, 'color matches')

    @patch.multiple(Shape, __abstractmethods__=set())
    def test_set_color(self):
        s = Shape(1, '#000001')
        s.color = '#111111'
        self.assertEqual('#111111', s.color, 'color matches')

    @patch.multiple(Shape, __abstractmethods__=set())
    def test_get_id(self):
        s = Shape(42, '#000001')
        self.assertEqual(42, s.shape_id, 'id matches')

    @patch.multiple(Shape, __abstractmethods__=set())
    def test_set_id(self):
        s = Shape(1, '#000001')
        s.shape_id = 42
        self.assertEqual(42, s.shape_id, 'id matches')

    @patch.multiple(Shape, __abstractmethods__=set())
    def test_move_by(self):
        a = Shape(1, '#000000')
        with self.assertRaises(NotImplementedError):
            a.move_by(Point(1, 2))

    @patch.multiple(Shape, __abstractmethods__=set())
    def test_accept_visitor(self):
        a = Shape(1, '#000000')
        with self.assertRaises(NotImplementedError):
            a.accept_visitor(Mock())

    @patch.multiple(Shape, __abstractmethods__=set())
    def test_contains_point(self):
        a = Shape(1, '#000000')
        with self.assertRaises(NotImplementedError):
            a.contains_point(Point(1, 2))

    @patch.multiple(Shape, __abstractmethods__=set())
    def test_repr(self):
        a = Shape(1, '#000000')
        with self.assertRaises(NotImplementedError):
            a.__repr__()

    @patch.multiple(Shape, __abstractmethods__=set())
    def test_str(self):
        a = Shape(1, '#000000')
        with self.assertRaises(NotImplementedError):
            a.__str__()
