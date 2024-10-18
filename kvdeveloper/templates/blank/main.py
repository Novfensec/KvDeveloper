import os
import importlib
from kivy.core.window import Window
from kivy import Config
from PIL import ImageGrab

resolution = ImageGrab.grab().size

# Change the values of the application window size as you need.
Config.set("graphics", "height", "690")
Config.set("graphics", "width", "317")

# Place the application window on the right side of the computer screen.
Window.top = 30
Window.left = resolution[0] - Window.width + 5

from kivymd.tools.hotreload.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

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
        self.theme_cls.primary_palette = "Midnightblue"

    def build_app(self) -> UI:
        self.manager_screens=UI()
        self.generate_application_screens()
        return self.manager_screens

    def generate_application_screens(self) -> None:
       # adds different screen widgets to the screen manager 
        import View.screens
        importlib.reload(View.screens)
        screens = View.screens.screens

        for i, name_screen in enumerate(screens.keys()):
            view = screens[name_screen]["object"]
            view.manager_screens = self.manager_screens
            view.name = name_screen
            self.manager_screens.add_widget(view)

if __name__ == '__main__':
    {{project_name}}().run()

'''
For Production uncomment the below code and comment out the above code
'''

# from kivymd.app import MDApp
# from kivymd.uix.screenmanager import MDScreenManager

# class UI(MDScreenManager):
#     def __init__(self, *args,**kwargs):
#         super(UI, self).__init__(*args,**kwargs)

# class {{project_name}}(MDApp):
#     def __init__(self, *args,**kwargs):
#         super({{project_name}}, self).__init__(*args,**kwargs)
#         self.load_all_kv_files(self.directory)
#         self.theme_cls.primary_palette = "Midnightblue"
#         self.manager_screens=UI()

#     def build(self) -> UI:
#         self.generate_application_screens()
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

# if __name__ == '__main__':
#     {{project_name}}().run()
