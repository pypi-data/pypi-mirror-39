from unittest import TestCase
from unittest.mock import Mock
import tkinter as tk

from caddy.view.application import Application
from caddy.view.buttons import ButtonFrame

class TestButtons(TestCase):

    def test_unregistered_button_handler(self):
        root = tk.Toplevel()
        app = Application(master=root)

        for event in ButtonFrame.ButtonEvents:
            app.button_menu.handle_button_click(event)

    def test_registered_button_handler(self):
        root = tk.Toplevel()
        app = Application(master=root)

        mock = Mock(return_value=4)

        for event in ButtonFrame.ButtonEvents:
            app.button_menu.register_button_handler(event, mock)

        for event in ButtonFrame.ButtonEvents:
            mock.reset_mock()
            res = app.button_menu.handle_button_click(event)
            mock.assert_called_once()
            self.assertEquals(res, 4)

    def test_handler_change(self):
        root = tk.Toplevel()
        app = Application(master=root)

        mock4 = Mock(return_value=4)
        mock7 = Mock(return_value=7)

        app.button_menu.register_button_handler(ButtonFrame.ButtonEvents.CURSOR, mock4)
        res = app.button_menu.handle_button_click(ButtonFrame.ButtonEvents.CURSOR)
        mock4.assert_called_once()
        self.assertEquals(res, 4)

        app.button_menu.register_button_handler(ButtonFrame.ButtonEvents.CURSOR, mock7)
        res = app.button_menu.handle_button_click(ButtonFrame.ButtonEvents.CURSOR)
        mock7.assert_called_once()
        self.assertEquals(res, 7)



