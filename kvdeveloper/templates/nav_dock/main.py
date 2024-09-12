import os
import importlib
from kivymd.tools.hotreload.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivy.core.window import Window
from kivy import Config
from PIL import ImageGrab
import webbrowser
from kvdeveloper.config import IMAGE_LIBRARY

resolution = ImageGrab.grab().size

# Change the values of the application window size as you need.
Config.set("graphics", "height", "690")
Config.set("graphics", "width", "317")

# Place the application window on the right side of the computer screen.
Window.top = 30
Window.left = resolution[0] - Window.width + 5

Window.keyboard_anim_args={"d": .2, "t": "in_out_expo"}
Window.softinput_mode="below_target"

class UI(MDScreenManager):
    def __init__(self, *args,**kwargs):
        super(UI, self).__init__(*args,**kwargs)

class {{project_name}}(MDApp):
    def __init__(self, *args,**kwargs):
        super({{project_name}}, self).__init__(*args,**kwargs)
        self.DEBUG=True
        self.KV_DIRS=[
            os.path.join(os.getcwd(),"View"),
        ]
        self.theme_cls.primary_palette="Indigo"
        self.theme_cls.primary_dark_hue="800"
        self.theme_cls.primary_light_hue="50"
        self.theme_cls.accent_palette="Indigo"
        self.theme_cls.accent_dark_hue="600"
        self.theme_cls.accent_light_hue="100"
        self.image_library_path=IMAGE_LIBRARY

    def build_app(self) -> UI:
        self.manager_screens=UI()
        self.generate_application_screens()
        return self.manager_screens

    def generate_application_screens(self) -> None:
        '''
        Adds different screen widgets to the screen manager
        '''
        import View.screens
        importlib.reload(View.screens)
        screens = View.screens.screens

        for i, name_screen in enumerate(screens.keys()):
            view = screens[name_screen]["object"]
            view.manager_screens = self.manager_screens
            view.name = name_screen
            self.manager_screens.add_widget(view)

    def web_open(self, url) -> None:
        webbrowser.open_new_tab(url)

if __name__ == '__main__':
    {{project_name}}().run()

'''
For Production uncomment the below code and comment out the above code
'''

# from kivymd.app import MDApp
# from kivymd.uix.screenmanager import MDScreenManager
# import webbrowser
# from kvdeveloper.config import IMAGE_LIBRARY
# from kivymd.utils.set_bars_colors import set_bars_colors
# from kivy.core.window import Window

# Window.keyboard_anim_args={"d": .2, "t": "in_out_expo"}
# Window.softinput_mode="below_target"

# class UI(MDScreenManager):
#     def __init__(self, *args,**kwargs):
#         super(UI, self).__init__(*args,**kwargs)

# class {{project_name}}(MDApp):
#     def __init__(self, *args,**kwargs):
#         super({{project_name}}, self).__init__(*args,**kwargs)
#         self.load_all_kv_files(self.directory)
#         self.theme_cls.primary_palette="Indigo"
#         self.theme_cls.primary_dark_hue="800"
#         self.theme_cls.primary_light_hue="50"
#         self.theme_cls.accent_palette="Indigo"
#         self.theme_cls.accent_dark_hue="600"
#         self.theme_cls.accent_light_hue="100"
#         self.image_library_path=IMAGE_LIBRARY
#         self.manager_screens=UI()
        
#     def build(self) -> UI:
#         self.generate_application_screens()
#         self.set_bars_colors()
#         return self.manager_screens
    
#     def generate_application_screens(self) -> None:
#        # adds different screen widgets to the screen manager 
#         import View.screens
#         screens = View.screens.screens

#         for i, name_screen in enumerate(screens.keys()):
#             view = screens[name_screen]["object"]
#             view.manager_screens = self.manager_screens
#             view.name = name_screen
#             self.manager_screens.add_widget(view)

#     def set_bars_colors(self) -> None:
#         set_bars_colors(
#             self.theme_cls.primary_color,  # status bar color
#             self.theme_cls.primary_color,  # navigation bar color
#             "Light",                       # icons color of status bar
#         )

#     def web_open(self, url) -> None:
#         webbrowser.open_new_tab(url)

# if __name__ == '__main__':
#     {{project_name}}().run()
