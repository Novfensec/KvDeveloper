from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.properties import StringProperty, BooleanProperty


class IconListItem(MDRelativeLayout):
    text = StringProperty()
    icon = StringProperty()
    secondary_text = StringProperty()
    ripple = BooleanProperty(True)
