from unittest import TestCase
from unittest.mock import MagicMock

from caddy.model.model import Model
from caddy.shared.point import Point


class TestModel(TestCase):

    def test_attach_observer(self):
        model = Model()
        observer = MagicMock()
        model.attach_observer(observer)
        model.add_circle(Point(1, 1), 5)
        observer.on_model_changed.assert_called_once()

    def test_detach_observer(self):
        model = Model()
        observer = MagicMock()
        model.attach_observer(observer)
        model.add_circle(Point(1, 1), 5)
        model.detach_observer(observer)
        model.add_circle(Point(1, 2), 6)
        observer.on_model_changed.assert_called_once()

    def test_add_circle(self):
        model = Model()
        shape_id = model.add_circle(Point(1, 1), 5)
        self.assertEqual(shape_id, model.shapes[0].shape_id, 'circle id matches')

    def test_add_rectangle(self):
        model = Model()
        shape_id = model.add_rectangle(Point(1, 1), Point(5, 4))
        self.assertEqual(shape_id, model.shapes[0].shape_id, 'rectangle id matches')

    def test_add_polyline(self):
        model = Model()
        shape_id = model.add_polyline([Point(1, 1)])
        self.assertEqual(shape_id, model.shapes[0].shape_id, 'polyline id matches')

    def test_remove_overlapping_with(self):
        model = Model()
        polyline_id = model.add_polyline([Point(1, 1), Point(3, 1)])
        rectangle1_id = model.add_rectangle(Point(0, 30), Point(20, 0))
        rectangle2_id = model.add_rectangle(Point(10, 15), Point(20, 5))
        circle_id = model.add_circle(Point(10, 10), 3)

        shape_ids = list(map(lambda s: s.shape_id, model.shapes))
        self.assertEqual([polyline_id, rectangle1_id, rectangle2_id, circle_id], shape_ids, 'shapes created')

        model.remove_overlapping_with(Point(1, 2))
        shape_ids = list(map(lambda s: s.shape_id, model.shapes))
        self.assertEqual([rectangle2_id, circle_id], shape_ids, 'shapes removed')

        model.remove_overlapping_with(Point(10, 8))
        shape_ids = list(map(lambda s: s.shape_id, model.shapes))
        self.assertEqual([], shape_ids, 'shapes removed')

    def test_overlapping_with(self):
        model = Model()
        polyline_id = model.add_polyline([Point(1, 1), Point(3, 1)])
        rectangle1_id = model.add_rectangle(Point(0, 30), Point(20, 0))
        rectangle2_id = model.add_rectangle(Point(10, 15), Point(20, 5))
        circle_id = model.add_circle(Point(10, 10), 3)

        shape_ids = list(map(lambda s: s.shape_id, model.shapes))
        self.assertEqual([polyline_id, rectangle1_id, rectangle2_id, circle_id], shape_ids, 'shapes created')

        shape_ids = list(map(lambda s: s.shape_id, model.overlapping_with(Point(1, 2))))
        self.assertEqual([polyline_id, rectangle1_id], shape_ids, 'shapes overlapping')

        shape_ids = list(map(lambda s: s.shape_id, model.overlapping_with(Point(10, 8))))
        self.assertEqual([rectangle1_id, rectangle2_id, circle_id], shape_ids, 'shapes overlapping')

        shape_ids = list(map(lambda s: s.shape_id, model.shapes))
        self.assertEqual([polyline_id, rectangle1_id, rectangle2_id, circle_id], shape_ids, 'shapes unchanged')

    def test_clear(self):
        model = Model()
        polyline_id = model.add_polyline([Point(1, 1), Point(3, 1)])
        rectangle_id = model.add_rectangle(Point(0, 30), Point(20, 30))

        shape_ids = list(map(lambda s: s.shape_id, model.shapes))
        self.assertEqual([polyline_id, rectangle_id], shape_ids, 'shapes created')

        model.clear()
        shape_ids = list(map(lambda s: s.shape_id, model.shapes))
        self.assertEqual([], shape_ids, 'shapes created')

    def test_move_by(self):
        model = Model()
        mock_shape1 = MagicMock()
        mock_shape2 = MagicMock()
        model.shapes = [mock_shape1, mock_shape2]
        point = Point(1, 1)
        offset = Point(1, 2)

        overlapping_mock = MagicMock(return_value=[mock_shape1, mock_shape2])
        model.overlapping_with = overlapping_mock
        model.move_by(point, offset)
        overlapping_mock.assert_called_once_with(point)
        mock_shape1.move_by.assert_called_once_with(offset)
        mock_shape2.move_by.assert_called_once_with(offset)

        overlapping_mock = MagicMock(return_value=[mock_shape2])
        model.overlapping_with = overlapping_mock
        model.move_by(point, offset)
        self.assertEqual(1, overlapping_mock.call_count)
        self.assertEqual(1, mock_shape1.move_by.call_count)
        self.assertEqual(2, mock_shape2.move_by.call_count)

    def test_accept_visitor(self):
        model = Model()
        visitor = MagicMock()
        model.add_polyline([Point(1, 1), Point(3, 1)])
        model.add_rectangle(Point(0, 30), Point(20, 30))
        model.add_circle(Point(10, 10), 3)
        model.accept_visitor(visitor)
        visitor.visit_polyline.assert_called_once()
        visitor.visit_rectangle.assert_called_once()
        visitor.visit_circle.assert_called_once()

    def test_update(self):
        model = Model()
        observer1 = MagicMock()
        observer2 = MagicMock()
        model.attach_observer(observer1)
        model.attach_observer(observer2)
        model._update()
        observer1.on_model_changed.assert_called_once()
        observer2.on_model_changed.assert_called_once()

    def test_find_by_id(self):
        model = Model()
        shape1 = MagicMock()
        shape1.shape_id = 1
        shape2 = MagicMock()
        shape2.shape_id = 2
        model.shapes = [shape1, shape2]
        self.assertEqual(shape1, model.find_by_id(1))
        self.assertEqual(shape2, model.find_by_id(2))

    def test_remove_by_id(self):
        model = Model()
        shape1 = MagicMock()
        shape1.shape_id = 1
        shape2 = MagicMock()
        shape2.shape_id = 2
        shape3 = MagicMock()
        shape3.shape_id = 3
        model.shapes = [shape1, shape2, shape3]
        model.remove_by_id(-1)
        self.assertEqual([1, 2, 3], list(map(lambda s: s.shape_id, model.shapes)))
        model.remove_by_id(2)
        self.assertEqual([1, 3], list(map(lambda s: s.shape_id, model.shapes)))
