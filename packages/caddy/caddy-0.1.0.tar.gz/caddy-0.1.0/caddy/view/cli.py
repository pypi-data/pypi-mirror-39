import tkinter as tk
from typing import Callable

from caddy.view.cli_interface import CLIInterface

class CLIFrame(tk.Frame, CLIInterface):

    def __init__(self, master:tk.Frame):
        super().__init__(master)
        self.handle_entry_function = lambda x: None
        self.entry = None
        self.text = None
        self.master = master
        self.cli_config()

    # ----- VIEW SETUP -------------------------------------------------------------------------------------------------

    def cli_config(self):
        text_frame = tk.Frame(self.master)
        text_frame.pack(side=tk.TOP, fill=tk.X)

        self.text = tk.Text(text_frame, background="#FFFFFF", state=tk.DISABLED, height=7, width=20, font=("Courier", 14))
        self.text.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.text.bind('<Button-1>', self.handle_unfocus)

        scrollbar = tk.Scrollbar(text_frame, command=self.text.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.text['yscrollcommand'] = scrollbar.set
        scrollbar.bind('<Button-1>', self.handle_unfocus)

        self.entry = tk.Entry(self.master, font=("Courier", 14))
        self.entry.pack(side=tk.TOP, fill=tk.X)
        self.entry.bind('<Return>', self.handle_entry_command)

    # ----- CLICK AND EVENT HANDLERS -----------------------------------------------------------------------------------

    def handle_entry_command(self, _):
        text = self.entry.get()
        if text == "":
            return
        self.entry.delete(0, tk.END)
        return self.handle_entry_function(text)

    def handle_unfocus(self, _=None):
        self.master.focus()

    # ----- HANDLER REGISTRATION ---------------------------------------------------------------------------------------

    def register_entry_handler(self, command: Callable):
        self.handle_entry_function = command

    # ----- VIEW MODIFICATION ------------------------------------------------------------------------------------------

    def add_text_command(self, command: str, command_result:str = ""):
        string = "> " + command + "\n"
        if command_result != "":
            string = string + command_result + "\n"
        self.text.config(state=tk.NORMAL)
        self.text.insert(tk.END, string)
        self.text.see(tk.END)
        self.text.config(state=tk.DISABLED)

    def add_text_command_result(self, result: str):
        string = result + "\n"
        self.text.config(state=tk.NORMAL)
        self.text.insert(tk.END, string)
        self.text.see(tk.END)
        self.text.config(state=tk.DISABLED)

    def cli_clear(self):
        self.entry.delete(0, tk.END)
        self.text.config(state=tk.NORMAL)
        self.text.delete(1.0, tk.END)
        self.text.config(state=tk.DISABLED)


    # ----- END CLASS --------------------------------------------------------------------------------------------------