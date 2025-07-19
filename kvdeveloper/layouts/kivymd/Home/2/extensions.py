from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.navigationrail import MDNavigationRailItem

napp = MDApp.get_running_app()


class BaseNavigationRailItem(MDNavigationRailItem):
    icon = StringProperty()
    text = StringProperty()
