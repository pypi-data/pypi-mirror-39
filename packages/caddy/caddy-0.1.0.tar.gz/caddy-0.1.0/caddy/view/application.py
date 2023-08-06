import tkinter as tk

from caddy.view.canvas import CanvasFrame
from caddy.view.cli import CLIFrame
from caddy.view.buttons import ButtonFrame
from caddy.view.menu import Menu

from caddy.view.application_interface import ApplicationInterface


class Application(tk.Frame, ApplicationInterface):

    def __init__(self, master=None):
        super().__init__(master)

        self.canvas = None
        self.cli = None
        self.button_menu = None
        self.main_menu = None
        self._title = "CAD"
        self._geometry = "800x610"

        self.master = master
        self.application_main_config()
        self.application_widgets_config()

    # ----- VIEW SETUP  ------------------------------------------------------------------------------------------------

    def application_main_config(self):
        self.master.title(self._title)
        self.master.geometry(self._geometry)
        self.master.resizable(width=False, height=False)
        self.pack()

    def application_widgets_config(self):
        main_menu = tk.Menu(self.master, relief=tk.FLAT)
        self.main_menu = Menu(main_menu)
        self.master.config(menu=main_menu)
        main_menu.bind('<Button-1>', self.entry_unfocus)

        button_frame = tk.Frame(self.master)
        button_frame.pack(side=tk.LEFT, fill=tk.Y)
        button_frame.bind('<Button-1>', self.entry_unfocus)
        self.button_menu = ButtonFrame(button_frame)

        layout_frame = tk.Frame(self.master)
        layout_frame.pack(side=tk.LEFT, fill=tk.BOTH)

        canvas_frame = tk.Frame(layout_frame)
        canvas_frame.pack(side=tk.TOP)
        self.canvas = CanvasFrame(canvas_frame, canvas_width=740, canvas_height=380)

        cli_frame = tk.Frame(layout_frame)
        cli_frame.pack(side=tk.TOP, fill=tk.BOTH)
        self.cli = CLIFrame(cli_frame)

    # ----- CLICKS AND EVENTS HANDLERS ---------------------------------------------------------------------------------

    def entry_unfocus(self, _=None):
        self.master.focus()

    # ----- END CLASS --------------------------------------------------------------------------------------------------
