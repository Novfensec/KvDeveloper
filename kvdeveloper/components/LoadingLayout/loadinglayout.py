from kivymd.uix.floatlayout import MDFloatLayout
from kivy.clock import mainthread


class LoadingLayout(MDFloatLayout):
    def __init__(self, *args, **kwargs):
        super(LoadingLayout, self).__init__(*args, **kwargs)

    @mainthread
    def display(self, timeout: int = None, *args) -> None:
        initial = 0
        if timeout:=timeout:
            while initial < timeout:
                self.opacity = 1
            self.opacity = 0
        self.opacity = 1

    @mainthread
    def dismiss(self, *args) -> None:
        self.opacity = 0
    