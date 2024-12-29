import os
import importlib
from kivy import Config
from PIL import ImageGrab

resolution = ImageGrab.grab().size

# Change the values of the application window size as you need.
Config.set("graphics", "height", "690")
Config.set("graphics", "width", "317")

from kivy.core.window import Window

# Place the application window on the right side of the computer screen.
Window.top = 30
Window.left = resolution[0] - Window.width + 5

import webbrowser
from kivymd.tools.hotreload.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.transition import MDSharedAxisTransition as SAT


class UI(MDScreenManager):
    def __init__(self, *args, **kwargs):
        super(UI, self).__init__(*args, **kwargs)
        self.transition = SAT()


class {{project_name}}(MDApp):
    def __init__(self, *args, **kwargs):
        super({{project_name}}, self).__init__(*args, **kwargs)
        self.DEBUG = True
        self.KV_DIRS = [
            os.path.join(os.getcwd(), "View"),
        ]
        self.theme_cls.primary_palette = "Midnightblue"

    def build_app(self) -> UI:
        self.manager_screens = UI()
        self.generate_application_screens()
        return self.manager_screens

    def generate_application_screens(self) -> None:
        """
        Adds different screen widgets to the screen manager
        """
        import View.screens

        importlib.reload(View.screens)
        screens = View.screens.screens

        for i, name_screen in enumerate(screens.keys()):
            view = screens[name_screen]["object"]()
            view.manager_screens = self.manager_screens
            view.name = name_screen
            self.manager_screens.add_widget(view)

    def apply_styles(self, style: str = "Light") -> None:
        self.theme_cls.theme_style = style

    def referrer(self, destination: str = None) -> None:
        if self.manager_screens.current != destination:
            self.manager_screens.current = destination

    def web_open(self, url: str) -> None:
        webbrowser.open_new_tab(url)


if __name__ == "__main__":
    {{project_name}}().run()
