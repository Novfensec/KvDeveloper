import os
import webbrowser
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.transition import MDSharedAxisTransition as SAT
from kivymd.utils.set_bars_colors import set_bars_colors
from kivy.core.window import Window
from kivy.clock import Clock


def set_softinput(*args) -> None:
    Window.keyboard_anim_args = {"d": 0.2, "t": "in_out_expo"}
    Window.softinput_mode = "below_target"


Window.on_restore(Clock.schedule_once(set_softinput, 0.1))


class UI(MDScreenManager):
    def __init__(self, *args, **kwargs):
        super(UI, self).__init__(*args, **kwargs)
        self.transition = SAT()


class {{project_name}}(MDApp):
    def __init__(self, *args, **kwargs):
        super({{project_name}}, self).__init__(*args, **kwargs)
        self.load_all_kv_files(os.path.join(self.directory, "View"))
        self.theme_cls.primary_palette = "Midnightblue"
        self.manager_screens = UI()

    def build(self) -> UI:
        self.generate_application_screens()
        self.apply_styles()
        return self.manager_screens

    def generate_application_screens(self) -> None:
        # adds different screen widgets to the screen manager
        import View.screens

        screens = View.screens.screens

        for i, name_screen in enumerate(screens.keys()):
            view = screens[name_screen]["object"]()
            view.manager_screens = self.manager_screens
            view.name = name_screen
            self.manager_screens.add_widget(view)

    def apply_styles(self, style: str = "Light") -> None:
        self.theme_cls.theme_style = style
        Window.clearcolor = self.theme_cls.backgroundColor
        if style == "Light":
            style = "Dark"
        self.set_bars_colors(style)

    def set_bars_colors(self, style: str = "Light") -> None:
        set_bars_colors(
            self.theme_cls.primaryColor,  # status bar color
            self.theme_cls.primaryColor,  # navigation bar color
            style,  # icons color of status bar
        )

    def referrer(self, destination: str = None) -> None:
        if self.manager_screens.current != destination:
            self.manager_screens.current = destination

    def web_open(self, url: str) -> None:
        webbrowser.open_new_tab(url)


if __name__ == "__main__":
    {{project_name}}().run()
