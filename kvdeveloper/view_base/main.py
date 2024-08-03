"""
Script for managing hot reloading of the project.
For more details see the documentation page -

https://kivymd.readthedocs.io/en/latest/api/kivymd/tools/patterns/create_project/

To run the application in hot boot mode, execute the command in the console:
set DEBUG=1 && python main.py
"""

import importlib
import os
from pathlib import Path

from kivy import Config
from PIL import ImageGrab

# TODO: You may know an easier way to get the size of a computer display.
resolution = ImageGrab.grab().size

# Change the values of the application window size as you need.
Config.set("graphics", "height", "715")
Config.set("graphics", "width", "317")

from kivy.core.window import Window

# Place the application window on the right side of the computer screen.
Window.top = 28
Window.left = resolution[0] - Window.width +3

from kivymd.tools.hotreload.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.utils.set_bars_colors import set_bars_colors
from kivy.clock import Clock

Clock.max_iteration=30

class {{project_name}}(MDApp):
    DEBUG=True
    KV_DIRS = [os.path.join(os.getcwd(), "View")]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette="Indigo"
        self.theme_cls.primary_dark_hue="800"
        self.theme_cls.primary_light_hue="50"
        self.theme_cls.accent_palette="Indigo"
        self.theme_cls.accent_dark_hue="600"
        self.theme_cls.accent_light_hue="100"
        self.apply_styles("Light")

    def build_app(self) -> MDScreenManager:
        """
        In this method, you don't need to change anything other than the
        application theme.
        """

        import View.screens

        self.manager_screens = MDScreenManager()
        Window.bind(on_key_down=self.on_keyboard_down)
        importlib.reload(View.screens)
        screens = View.screens.screens

        for i, name_screen in enumerate(screens.keys()):
            model = screens[name_screen]["model"]()
            controller = screens[name_screen]["controller"](model)
            view = controller.get_view()
            view.manager_screens = self.manager_screens
            view.name = name_screen
            self.manager_screens.add_widget(view)
            
        return self.manager_screens

    def apply_styles(self,style="Light"):
        self.theme_cls.theme_style=style
        
    def on_keyboard_down(self, window, keyboard, keycode, text, modifiers) -> None:
        """
        The method handles keyboard events.

        By default, a forced restart of an application is tied to the
        `CTRL+R` key on Windows OS and `COMMAND+R` on Mac OS.
        """

        if "meta" in modifiers or "ctrl" in modifiers and text == "r":
            self.rebuild()

if __name__ == '__main__':
    {{project_name}}().run()

# After you finish the project, remove the above code and uncomment the below
# code to test the application normally without hot reloading.

# """
# The entry point to the application.
# 
# The application uses the MVC template. Adhering to the principles of clean
# architecture means ensuring that your application is easy to test, maintain,
# and modernize.
# 
# You can read more about this template at the links below:
# 
# https://github.com/HeaTTheatR/LoginAppMVC
# https://en.wikipedia.org/wiki/Model–view–controller
# """
# 
# from kivymd.app import MDApp
# from kivymd.uix.screenmanager import MDScreenManager
# from kivymd.utils.set_bars_colors import set_bars_colors

# from kivy.clock import Clock

# Clock.max_iteration=30

# from View.screens import screens

# from PIL import ImageGrab

# # TODO: You may know an easier way to get the size of a computer display.
# resolution = ImageGrab.grab().size

# # Change the values of the application window size as you need.


# from kivy.core.window import Window

# # Place the application window on the right side of the computer screen.
# Window.top = 30
# Window.left = resolution[0] - Window.width

# class {{project_name}}(MDApp):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.load_all_kv_files(self.directory)
#         self.theme_cls.primary_palette="Indigo"
#         self.theme_cls.primary_dark_hue="800"
#         self.theme_cls.primary_light_hue="50"
#         self.theme_cls.accent_palette="Indigo"
#         self.theme_cls.accent_dark_hue="600"
#         self.theme_cls.accent_light_hue="100"
#         self.apply_styles("Light")
#         # This is the screen manager that will contain all the screens of your
#         # application.
#         self.manager_screens = MDScreenManager()
        
#     def build(self) -> MDScreenManager:
#         self.generate_application_screens()
#         self.set_bars_colors()
#         self.manager_screens.padding="44dp"
#         self.manager_screens.current="home screen"
#         self.manager_screens.transition=MDSwapTransition()
#         return self.manager_screens

#     def generate_application_screens(self) -> None:
#         """
#         Creating and adding screens to the screen manager.
#         You should not change this cycle unnecessarily. He is self-sufficient.

#         If you need to add any screen, open the `View.screens.py` module and
#         see how new screens are added according to the given application
#         architecture.
#         """

#         for i, name_screen in enumerate(screens.keys()):
#             model = screens[name_screen]["model"]()
#             controller = screens[name_screen]["controller"](model)
#             view = controller.get_view()
#             view.manager_screens = self.manager_screens
#             view.name = name_screen
#             self.manager_screens.add_widget(view)

#     def set_bars_colors(self):
#         set_bars_colors(
#             self.theme_cls.primary_color,  # status bar color
#             self.theme_cls.primary_color,  # navigation bar color
#             "Light",                       # icons color of status bar
#         )

#     def apply_styles(self,style="Light"):
#         self.theme_cls.theme_style=style

# if __name__ == '__main__':
#     {{project_name}}().run()