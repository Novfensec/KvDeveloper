from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen


class BaseScreenView(MDScreen):

    manager_screens = ObjectProperty()
    """
    Screen manager object - :class:`~kivymd.uix.screenmanager.MDScreenManager`.

    :attr:`manager_screens` is an :class:`~kivy.properties.ObjectProperty`
    and defaults to `None`.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Often you need to get access to the application object from the view
        # class. You can do this using this attribute.
        self.app = MDApp.get_running_app()
