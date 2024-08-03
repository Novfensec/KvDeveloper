from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.screen import MDScreen
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.boxlayout import MDBoxLayout

class ContentNavigationDrawer(MDNavigationDrawer):
    def __init__(self, *args, **kwargs):
        super(ContentNavigationDrawer, self).__init__( *args, **kwargs)

class ContentNavigationLayout(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super(ContentNavigationLayout, self).__init__( *args, **kwargs) 

class BaseScreenView(ThemableBehavior, MDScreen):
    
    manager_screens = ObjectProperty()
    """
    Screen manager object - :class:`~kivymd.uix.screenmanager.MDScreenManager`.

    :attr:`manager_screens` is an :class:`~kivy.properties.ObjectProperty`
    and defaults to `None`.
    """

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        # Often you need to get access to the application object from the view
        # class. You can do this using this attribute.
        self.app = MDApp.get_running_app()
