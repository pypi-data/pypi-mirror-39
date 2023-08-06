import tkinter as tk
from typing import Callable

from caddy.view.canvas_interface import CanvasInterface

class CanvasFrame(tk.Frame, CanvasInterface):

    def __init__(self, master:tk.Frame, canvas_width:int=740, canvas_height:int=380):
        super().__init__(master)

        self.handle_canvas_click_function = lambda x: None
        self.canvas = None
        self.state_indicator = None
        self.cursor_position_indicator = None
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.master = master

        self.canvas_config()

    # ----- VIEW SETUP -------------------------------------------------------------------------------------------------

    def canvas_config(self):
        self.canvas = tk.Canvas(self.master, width=self.canvas_width, height=self.canvas_height, background="#FFFFFF")
        self.canvas.pack(expand=True)
        self.canvas.bind('<Button-1>', self.handle_canvas_click)
        self.canvas.bind('<Motion>', self.handle_cursor_position)
        self.canvas.bind('<Leave>', self.handle_canvas_leave)
        status_frame = tk.Frame(self.master)
        status_frame.pack(fill=tk.X)
        status_frame.bind('<Button-1>', self.handle_unfocus)
        self.state_indicator = tk.Label(status_frame, text="", pady=4)
        self.state_indicator.bind('<Button-1>', self.handle_unfocus)
        self.state_indicator.pack(side=tk.LEFT)
        self.cursor_position_indicator = tk.Label(status_frame, text="")
        self.cursor_position_indicator.bind('<Button-1>', self.handle_unfocus)
        self.cursor_position_indicator.pack(side=tk.RIGHT)

    # ----- CLICK AND EVENT HANDLERS -----------------------------------------------------------------------------------

    def handle_canvas_click(self, event):
        self.handle_unfocus()
        return self.handle_canvas_click_function(self.transform_coords_technical_normal((event.x, event.y)))

    def handle_unfocus(self, _=None):
        self.master.focus()

    def handle_cursor_position(self, event):
        self.set_cursor_position_indicator(self.transform_coords_technical_normal((event.x, event.y)))

    def handle_canvas_leave(self, _=None):
        self.unset_cursor_position_indicator()

    # ----- HANDLER REGISTRATION ---------------------------------------------------------------------------------------

    def register_canvas_click_handler(self, command: Callable):
        self.handle_canvas_click_function = command

    # ----- CANVAS MODIFICATION ----------------------------------------------------------------------------------------

    def transform_coords_technical_normal(self, coords: tuple) -> tuple:
        x, y = coords
        return x, self.canvas_height - y

    def add_line(self, coords_a: tuple, coords_b: tuple):
        a = self.transform_coords_technical_normal(coords_a)
        b = self.transform_coords_technical_normal(coords_b)
        self.canvas.create_line(a, b)

    def add_rectangle(self, coords_a: tuple, coords_b: tuple):
        a = self.transform_coords_technical_normal(coords_a)
        b = self.transform_coords_technical_normal(coords_b)
        self.canvas.create_rectangle(a, b)

    def add_circle(self, center: tuple, r: int):
        center_transformed = self.transform_coords_technical_normal(center)
        a = (center_transformed[0] - r, center_transformed[1] - r)
        b = (center_transformed[0] + r, center_transformed[1] + r)
        self.canvas.create_oval(a, b)

    def canvas_clear(self):
        self.canvas.delete("all")

    # ----- STATUS BAR MODIFICATION ------------------------------------------------------------------------------------

    def set_state_indicator(self, text:str):
        self.state_indicator.config(text=text)

    def set_cursor_position_indicator(self, position: tuple):
        text = "[" + str(position[0]) + "," + str(position[1]) + "]"
        self.cursor_position_indicator.config(text=text)

    def unset_cursor_position_indicator(self):
        self.cursor_position_indicator.config(text="")

    # ----- END CLASS --------------------------------------------------------------------------------------------------

