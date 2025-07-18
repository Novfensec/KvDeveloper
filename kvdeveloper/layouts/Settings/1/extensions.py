from kivy.properties import BooleanProperty, StringProperty
from kivymd.uix.relativelayout import MDRelativeLayout


class IconListItem(MDRelativeLayout):
    text = StringProperty()
    icon = StringProperty()
    secondary_text = StringProperty()
    ripple = BooleanProperty(True)
