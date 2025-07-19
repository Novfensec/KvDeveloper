import os
import webbrowser

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.resources import resource_add_path

from {{app_module}}import {{app_class}}
from {{screenmanager_module}} import {{screenmanager_class}}

def set_softinput(*args) -> None:
    Window.keyboard_anim_args = {"d": 0.2, "t": "in_out_expo"}
    Window.softinput_mode = "below_target"


Window.on_restore(Clock.schedule_once(set_softinput, 0.1))


class UI({{screenmanager_class}}):
    def __init__(self, *args, **kwargs):
        super(UI, self).__init__(*args, **kwargs)


class {{project_name}}({{app_class}}):

    def __init__(self, *args, **kwargs):
        super({{project_name}}, self).__init__(*args, **kwargs)
        resource_add_path(self.directory)
        # self.load_all_kv_files(os.path.join(self.directory, "View"))
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
        # do theme styling accordingly
        Window.clearcolor = [1, 1, 1, 1]

    def referrer(self, destination: str = None) -> None:
        if self.manager_screens.current != destination:
            self.manager_screens.current = destination

    def web_open(self, url: str) -> None:
        webbrowser.open_new_tab(url)


if __name__ == "__main__":
    app = {{project_name}}()
    app.run()
