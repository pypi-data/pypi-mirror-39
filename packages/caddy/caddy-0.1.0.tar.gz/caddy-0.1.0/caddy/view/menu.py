import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as msg
from typing import Callable

from caddy.view.menu_interface import MenuInterface

class Menu(tk.Menu, MenuInterface):

    def __init__(self, master:tk.Menu):
        super().__init__(master)

        self.menu_handlers = { event.value : (lambda x=None: None)
                                 for event in self.MenuEvents }
        self.maser = master
        self.main_menu_config()

    # ----- VIEW SETUP -------------------------------------------------------------------------------------------------

    def main_menu_config(self):
        filemenu = tk.Menu(self.master, tearoff=0)
        filemenu.add_command(label="New", command=lambda: self.handle_menu_click_new())
        filemenu.add_command(label="Load", command=lambda: self.handle_menu_click_load())
        filemenu.add_command(label="Save as...", command=lambda: self.handle_menu_click_saveas())
        filemenu.add_command(label="Exit", command=lambda: self.handle_menu_click_exit())
        self.master.add_cascade(menu=filemenu, label="File")

        helpmenu = tk.Menu(self.master, tearoff=0)
        helpmenu.add_command(label="Display help")
        self.master.add_cascade(menu=helpmenu, label="Help")

    # ----- CLICKS AND EVENTS HANDLERS ---------------------------------------------------------------------------------

    def handle_menu_click_new(self):
        res = msg.askokcancel("Open new file","Do you really want to open new file?")
        if res:
            self.menu_handlers[self.MenuEvents.NEW.value]()

    def handle_menu_click_load(self):
        file = fd.askopenfilename(parent=self.master,
                                  filetypes=(("CAD Files","*.cad"),("All Files","*.*")))

        # catch values that are the results of file dialog when clicked on cancel or close
        if file != "" and file != ():
            self.menu_handlers[self.MenuEvents.LOAD.value](file)

    def handle_menu_click_saveas(self):
        file = fd.asksaveasfilename(parent=self.master,
                                    filetypes=(("CAD Files","*.cad"),("All Files","*.*")),
                                    defaultextension='.cad')

        # catch values that are the results of file dialog when clicked on cancel or close
        if file != "" and file != ():
            self.menu_handlers[self.MenuEvents.SAVEAS.value](file)

    def handle_menu_click_exit(self):
        res = msg.askokcancel("Exit", "Do you really want to quit?")
        if res:
            self.menu_handlers[self.MenuEvents.EXIT.value]()


    # ----- HANDLER REGISTRATION ---------------------------------------------------------------------------------------

    def register_menu_handler(self, menu_event: MenuInterface.MenuEvents, command: Callable):
        try:
            self.menu_handlers[menu_event.value] = command
        except KeyError:
            raise ValueError("Invalid event")

    # ----- END CLASS --------------------------------------------------------------------------------------------------
