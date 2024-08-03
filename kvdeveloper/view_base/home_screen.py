from View.base_screen import BaseScreenView
from kivymd.uix.boxlayout import MDBoxLayout

class HomeScreenContext(MDBoxLayout):
    pass

class HomeScreenView(BaseScreenView):
    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """