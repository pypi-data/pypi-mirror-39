import tkinter as tk

from caddy.model.model import Model
from caddy.presenter.presenter import Presenter
from caddy.view.application import Application
from caddy.view.buttons import ButtonFrame
from caddy.view.menu import Menu


def main():
    root = tk.Tk()
    app = Application(master=root)

    app.button_menu.register_button_handler(ButtonFrame.ButtonEvents.LIST, lambda: print("Clicked on list"))

    app.main_menu.register_menu_handler(Menu.MenuEvents.NEW, lambda: print("Clicked on new"))
    app.main_menu.register_menu_handler(Menu.MenuEvents.LOAD, lambda x: print("Clicked on load:", x))
    app.main_menu.register_menu_handler(Menu.MenuEvents.SAVEAS, lambda x: print("Clicked on save as file:", x))
    app.main_menu.register_menu_handler(Menu.MenuEvents.EXIT, lambda: print("Clicked on exit"))

    app.cli.register_entry_handler(lambda txt: app.cli.add_text_command(txt))

    model = Model()
    Presenter(model, app)

    app.mainloop()


if __name__ == '__main__':  # pragma: no cover
    main()
