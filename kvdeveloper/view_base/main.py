# After you finish the project, remove the above code and uncomment the below
# code to test the application normally without hot reloading.

"""
The entry point to the application.

The application uses the MVC template. Adhering to the principles of clean
architecture means ensuring that your application is easy to test, maintain,
and modernize.

You can read more about this template at the links below:

https://github.com/HeaTTheatR/LoginAppMVC
https://en.wikipedia.org/wiki/Model–view–controller
"""

# ==========================
# Standard Library Imports
# ==========================
import os
import ssl
import webbrowser


# ==========================
# Third-Party Library Imports
# ==========================
from kivy.clock import Clock
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.transition import MDSharedAxisTransition as SAT
from kivymd.utils.set_bars_colors import set_bars_colors


# ==========================
# Custom Module Imports
# ==========================
from View.screens import screens


# ==========================
# SSL Configuration
# ==========================
ssl._create_default_https_context = ssl._create_unverified_context


Clock.max_iteration = 30


def set_softinput(*args) -> None:
    Window.keyboard_anim_args = {"d": 0.2, "t": "in_out_expo"}
    Window.softinput_mode = "below_target"


Window.on_restore(Clock.schedule_once(set_softinput, 0.1))


class UI(MDScreenManager):
    def __init__(self, *args, **kwargs):
        super(UI, self).__init__(*args, **kwargs)
        self.transition = SAT()


class {{project_name}}(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_all_kv_files(os.path.join(self.directory, "View"))
        self.theme_cls.primary_palette = "Darkgrey"
        # This is the screen manager that will contain all the screens of your application.
        self.manager_screens = UI()

    def build(self) -> UI:
        self.generate_application_screens()
        self.apply_styles("Light")
        return self.manager_screens

    def generate_application_screens(self) -> None:
        """
        Creating and adding screens to the screen manager.
        You should not change this cycle unnecessarily. He is self-sufficient.

        If you need to add any screen, open the `View.screens` module and
        see how new screens are added according to the given application
        architecture.
        """

        for i, name_screen in enumerate(screens.keys()):
            model = screens[name_screen]["model"]()
            controller = screens[name_screen]["controller"](model)
            view = controller.get_view()
            view.manager_screens = self.manager_screens
            view.name = name_screen
            self.manager_screens.add_widget(view)

    def apply_styles(self, style: str = "Light") -> None:
        self.theme_cls.theme_style = style
        if style == "Light":
            style = "Dark"
        else:
            style = "Light"
        Window.clearcolor = status_color = nav_color = self.theme_cls.backgroundColor
        self.set_bars_colors(status_color, nav_color, style)

    def set_bars_colors(self, status_color: list[float] = [1.0, 1.0, 1.0, 1.0], nav_color: list[float] = [1.0, 1.0, 1.0, 1.0], style: str = "Light") -> None:
        set_bars_colors(
            status_color,  # status bar color
            nav_color,  # navigation bar color
            style,  # icons color of status and navigation bar
        )

    def referrer(self, destination: str = None) -> None:
        if self.manager_screens.current != destination:
            self.manager_screens.current = destination

    def web_open(self, url: str) -> None:
        webbrowser.open_new_tab(url)


if __name__ == "__main__":
    {{project_name}}().run()
