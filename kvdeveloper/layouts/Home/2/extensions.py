from kivymd.app import MDApp
from kivymd.uix.navigationrail import MDNavigationRailItem
from kivy.properties import StringProperty

napp = MDApp.get_running_app()
    
class BaseNavigationRailItem(MDNavigationRailItem):
    icon = StringProperty()
    text = StringProperty()