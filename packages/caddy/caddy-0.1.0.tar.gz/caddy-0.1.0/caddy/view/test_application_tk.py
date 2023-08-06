from unittest import TestCase
import tkinter as tk

from caddy.view.application import Application

from caddy.view.canvas import CanvasFrame
from caddy.view.cli import CLIFrame
from caddy.view.buttons import ButtonFrame
from caddy.view.menu import Menu

class TestApplication(TestCase):

    def test_get_components(self):
        root = tk.Toplevel()
        app = Application(master=root)

        menu, buttons, canvas, cli = app.get_components()

        self.assertEquals(type(menu), Menu)
        self.assertEquals(type(buttons), ButtonFrame)
        self.assertEquals(type(canvas), CanvasFrame)
        self.assertEquals(type(cli), CLIFrame)
