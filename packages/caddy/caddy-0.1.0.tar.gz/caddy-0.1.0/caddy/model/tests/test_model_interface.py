from unittest import TestCase
from unittest.mock import patch, Mock

from caddy.model.model_interface import ModelInterface


class TestModelInterface(TestCase):
    @patch.multiple(ModelInterface, __abstractmethods__=set())
    def test_attach_observer(self):
        m = ModelInterface()
        with self.assertRaises(NotImplementedError):
            m.attach_observer(Mock())

    @patch.multiple(ModelInterface, __abstractmethods__=set())
    def test_detach_observer(self):
        m = ModelInterface()
        with self.assertRaises(NotImplementedError):
            m.detach_observer(Mock())

    @patch.multiple(ModelInterface, __abstractmethods__=set())
    def test_add_circle(self):
        m = ModelInterface()
        with self.assertRaises(NotImplementedError):
            m.add_circle(Mock(), 1)

    @patch.multiple(ModelInterface, __abstractmethods__=set())
    def test_add_rectangle(self):
        m = ModelInterface()
        with self.assertRaises(NotImplementedError):
            m.add_rectangle(Mock(), 1, 1)

    @patch.multiple(ModelInterface, __abstractmethods__=set())
    def test_add_polyline(self):
        m = ModelInterface()
        with self.assertRaises(NotImplementedError):
            m.add_polyline(Mock())

    @patch.multiple(ModelInterface, __abstractmethods__=set())
    def test_remove_overlapping_with(self):
        m = ModelInterface()
        with self.assertRaises(NotImplementedError):
            m.remove_overlapping_with(Mock())

    @patch.multiple(ModelInterface, __abstractmethods__=set())
    def test_overlapping_with(self):
        m = ModelInterface()
        with self.assertRaises(NotImplementedError):
            m.overlapping_with(Mock())

    @patch.multiple(ModelInterface, __abstractmethods__=set())
    def test_find_by_id(self):
        m = ModelInterface()
        with self.assertRaises(NotImplementedError):
            m.find_by_id(1)

    @patch.multiple(ModelInterface, __abstractmethods__=set())
    def test_clear(self):
        m = ModelInterface()
        with self.assertRaises(NotImplementedError):
            m.clear()

    @patch.multiple(ModelInterface, __abstractmethods__=set())
    def test_move_by(self):
        m = ModelInterface()
        with self.assertRaises(NotImplementedError):
            m.move_by(Mock(), Mock())

    @patch.multiple(ModelInterface, __abstractmethods__=set())
    def test_accept_visitor(self):
        m = ModelInterface()
        with self.assertRaises(NotImplementedError):
            m.accept_visitor(Mock())
