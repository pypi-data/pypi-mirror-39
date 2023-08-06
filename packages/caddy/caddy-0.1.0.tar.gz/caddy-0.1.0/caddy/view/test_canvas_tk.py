from unittest import TestCase
from unittest.mock import Mock
import tkinter as tk

from caddy.view.application import Application

class TestCanvas(TestCase):

    def test_unregistered_canvas_click_handler(self):
        root = tk.Toplevel()
        app = Application(master=root)

        mock = Mock()
        mock.x = 45
        mock.y = 741

        app.canvas.handle_canvas_click(mock)

    def test_registered_canvas_click_handler(self):
        def test_function(coords):
            return coords

        root = tk.Toplevel()
        app = Application(master=root)

        mock = Mock(x=405, y=41)
        app.canvas.register_canvas_click_handler(test_function)
        res = app.canvas.handle_canvas_click(mock)
        self.assertEquals(res, app.canvas.transform_coords_technical_normal((405, 41)))
        mock = Mock(x=0, y=200)
        res = app.canvas.handle_canvas_click(mock)
        self.assertEquals(res, app.canvas.transform_coords_technical_normal((0, 200)))

    def test_canvas_click_handler_change(self):
        def test_function_a(coords):
            return 0, 0
        def test_function_b(coords):
            return 10, 20

        root = tk.Toplevel()
        app = Application(master=root)

        mock = Mock(x=405, y=41)
        app.canvas.register_canvas_click_handler(test_function_a)
        res = app.canvas.handle_canvas_click(mock)
        self.assertEquals(res, (0, 0))
        app.canvas.register_canvas_click_handler(test_function_b)
        res = app.canvas.handle_canvas_click(mock)
        self.assertEquals(res, (10, 20))

    def test_transform_coords(self):
        root = tk.Toplevel()
        app = Application(master=root)

        canvas_height = app.canvas.canvas_height

        res = app.canvas.transform_coords_technical_normal((0, 0))
        self.assertEquals(res, (0, canvas_height - 0))
        res = app.canvas.transform_coords_technical_normal((app.canvas.canvas_width, canvas_height))
        self.assertEquals(res, (app.canvas.canvas_width, 0))
        res = app.canvas.transform_coords_technical_normal((50, 150))
        self.assertEquals(res, (50, canvas_height - 150))
        res = app.canvas.transform_coords_technical_normal((app.canvas.canvas_width + 100, canvas_height + 100))
        self.assertEquals(res, (app.canvas.canvas_width + 100, -100))

    def test_set_state_indicator(self):
        root = tk.Toplevel()
        app = Application(master=root)

        app.canvas.set_state_indicator("test")
        self.assertEquals(app.canvas.state_indicator["text"], "test")
        app.canvas.set_state_indicator("test test test")
        self.assertEquals(app.canvas.state_indicator["text"], "test test test")
        app.canvas.set_state_indicator("")
        self.assertEquals(app.canvas.state_indicator["text"], "")

    def test_set_cursor_indicator(self):
        root = tk.Toplevel()
        app = Application(master=root)

        app.canvas.set_cursor_position_indicator((0, 0))
        self.assertEquals(app.canvas.cursor_position_indicator["text"], "[0,0]")
        app.canvas.set_cursor_position_indicator((1000, 1000))
        self.assertEquals(app.canvas.cursor_position_indicator["text"], "[1000,1000]")
        app.canvas.set_cursor_position_indicator((72, 250))
        self.assertEquals(app.canvas.cursor_position_indicator["text"], "[72,250]")

    def test_unset_cursor_indicator(self):
        root = tk.Toplevel()
        app = Application(master=root)

        app.canvas.set_cursor_position_indicator((0, 0))
        self.assertEquals(app.canvas.cursor_position_indicator["text"], "[0,0]")
        app.canvas.unset_cursor_position_indicator()
        self.assertEquals(app.canvas.cursor_position_indicator["text"], "")
        app.canvas.set_cursor_position_indicator((72, 250))
        self.assertEquals(app.canvas.cursor_position_indicator["text"], "[72,250]")
        app.canvas.unset_cursor_position_indicator()
        self.assertEquals(app.canvas.cursor_position_indicator["text"], "")

    def test_add_line(self):
        root = tk.Toplevel()
        app = Application(master=root)
        canvas_height = app.canvas.canvas_height
        app.canvas.add_line((10, 23), (20, 55))
        app.canvas.add_line((0, 0), (0, 0))
        app.canvas.add_line((1000, 2000), (1, 5))

        self.assertEquals(len(app.canvas.canvas.find_all()), 3)

        line_tag = app.canvas.canvas.find_all()[0]
        self.assertEquals(app.canvas.canvas.coords(line_tag), [10, canvas_height - 23, 20, canvas_height - 55])
        line_tag = app.canvas.canvas.find_all()[1]
        self.assertEquals(app.canvas.canvas.coords(line_tag), [0, canvas_height - 0, 0, canvas_height - 0])
        line_tag = app.canvas.canvas.find_all()[2]
        self.assertEquals(app.canvas.canvas.coords(line_tag), [1000, canvas_height - 2000, 1, canvas_height - 5])

    def test_add_rectangle(self):
        root = tk.Toplevel()
        app = Application(master=root)
        canvas_height = app.canvas.canvas_height
        app.canvas.add_rectangle((10, 23), (20, 55))
        app.canvas.add_rectangle((0, 0), (0, 0))
        app.canvas.add_rectangle((1000, 2000), (1, 5))
        app.canvas.add_rectangle((0, 10), (10, 0))

        self.assertEquals(len(app.canvas.canvas.find_all()), 4)

        line_tag = app.canvas.canvas.find_all()[0]
        self.assertEquals(app.canvas.canvas.coords(line_tag), [10, canvas_height - 55, 20, canvas_height - 23])
        line_tag = app.canvas.canvas.find_all()[1]
        self.assertEquals(app.canvas.canvas.coords(line_tag), [0, canvas_height - 0, 0, canvas_height - 0])
        line_tag = app.canvas.canvas.find_all()[2]
        self.assertEquals(app.canvas.canvas.coords(line_tag), [1, canvas_height - 2000, 1000, canvas_height - 5])
        line_tag = app.canvas.canvas.find_all()[3]
        self.assertEquals(app.canvas.canvas.coords(line_tag), [0, canvas_height - 10, 10, canvas_height - 0])

    def test_add_circle(self):
        root = tk.Toplevel()
        app = Application(master=root)
        canvas_height = app.canvas.canvas_height
        app.canvas.add_circle((0, 0), 4)
        app.canvas.add_circle((10, 20), 10)
        app.canvas.add_circle((1000, 2000), 1050)

        self.assertEquals(len(app.canvas.canvas.find_all()), 3)

        line_tag = app.canvas.canvas.find_all()[0]
        self.assertEquals(app.canvas.canvas.coords(line_tag), [-4, canvas_height-4, 4, canvas_height+4])
        line_tag = app.canvas.canvas.find_all()[1]
        self.assertEquals(app.canvas.canvas.coords(line_tag), [0, canvas_height-30, 20, canvas_height-10])
        line_tag = app.canvas.canvas.find_all()[2]
        self.assertEquals(app.canvas.canvas.coords(line_tag), [-50, canvas_height-3050, 2050, canvas_height-950])

    def test_clear_canvas(self):
        root = tk.Toplevel()
        app = Application(master=root)
        app.canvas.add_line((10, 23), (20, 55))
        app.canvas.add_circle((0, 0), 4)
        app.canvas.add_rectangle((0, 10), (10, 0))
        self.assertEquals(len(app.canvas.canvas.find_all()), 3)
        app.canvas.canvas_clear()
        self.assertEquals(len(app.canvas.canvas.find_all()), 0)

    def test_handle_cursor_position(self):
        root = tk.Toplevel()
        app = Application(master=root)

        mock = Mock(x=0, y=app.canvas.canvas_height)
        app.canvas.handle_cursor_position(mock)
        self.assertEquals(app.canvas.cursor_position_indicator["text"], "[0,0]")
        mock = Mock(x=145, y=186)
        app.canvas.handle_cursor_position(mock)
        self.assertEquals(app.canvas.cursor_position_indicator["text"], "[145,"+ str(app.canvas.canvas_height - 186) +"]")

    def test_handle_canvas_leave(self):
        root = tk.Toplevel()
        app = Application(master=root)

        mock = Mock(x=0, y=app.canvas.canvas_height)
        app.canvas.handle_cursor_position(mock)
        self.assertEquals(app.canvas.cursor_position_indicator["text"], "[0,0]")
        app.canvas.handle_canvas_leave()
        self.assertEquals(app.canvas.cursor_position_indicator["text"], "")
