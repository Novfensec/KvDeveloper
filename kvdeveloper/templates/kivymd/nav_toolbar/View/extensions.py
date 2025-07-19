from kivy.properties import StringProperty
from kivymd.uix.navigationdrawer import MDNavigationDrawerItem
from kivymd.uix.textfield import MDTextField


class DrawerClickableItem(MDNavigationDrawerItem):
    icon = StringProperty()
    text = StringProperty()


class CustomTextField(MDTextField):
    icon_left = StringProperty()
    hint_text = StringProperty()
    helper_text = StringProperty()
