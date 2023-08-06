import os
import tkinter as tk
from typing import Callable

from caddy.view.button_interface import ButtonInterface


class ButtonFrame(tk.Frame, ButtonInterface):

    def __init__(self, master:tk.Frame):
        super().__init__(master)

        self.button_handlers = { event.value : (lambda: None)
                                 for event in self.ButtonEvents }
        self.maser = master
        self.button_menu_config()

    # ----- VIEW SETUP -------------------------------------------------------------------------------------------------

    def button_menu_config(self):

        def create_menu_button(btn_event: ButtonFrame.ButtonEvents):
            package_directory = os.path.dirname(os.path.abspath(__file__))
            button_img = tk.PhotoImage(file=os.path.join(package_directory, 'icons', btn_event.value + '.png'))
            button = tk.Button(self.master, width=40, height=40, image=button_img,
                               command= lambda: self.handle_button_click(btn_event))
            button.photo = button_img
            button.pack(side=tk.TOP)

        for event in self.ButtonEvents:
            create_menu_button(event)

    # ----- CLICKS AND EVENTS HANDLERS ---------------------------------------------------------------------------------

    def handle_button_click(self, command_name: ButtonInterface.ButtonEvents):
        self.handle_unfocus()
        try:
            return self.button_handlers[command_name.value]()
        except KeyError:
            raise ValueError("Invalid event")

    def handle_unfocus(self):
        self.master.focus()

    # ----- HANDLER REGISTRATION ---------------------------------------------------------------------------------------

    def register_button_handler(self, button_event: ButtonInterface.ButtonEvents, command: Callable):
        try:
            self.button_handlers[button_event.value] = command
        except KeyError:
            raise ValueError("Invalid event")

    # ----- END CLASS --------------------------------------------------------------------------------------------------
