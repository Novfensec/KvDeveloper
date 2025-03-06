from kivymd.app import MDApp
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem
from kivy.properties import StringProperty

napp = MDApp.get_running_app()


def on_switch_tabs(
    self, bar: MDNavigationBar, item_icon: str, item_text: str, sub_manager_screens
):
    sub_manager_screens.current = item_text.lower()


class BaseNavigationItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()
    ripple_effect = False
