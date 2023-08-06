from unittest import TestCase
from unittest.mock import patch

from caddy.model.model_interface import ModelObserver


class TestModelObserver(TestCase):

    def test_cannot_instantiate(self):
        with self.assertRaises(TypeError):
            ModelObserver()

    @patch.multiple(ModelObserver, __abstractmethods__=set())
    def test_on_model_changed(self):
        m = ModelObserver()
        with self.assertRaises(NotImplementedError):
            m.on_model_changed()
