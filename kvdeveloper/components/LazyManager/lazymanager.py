import os, glob

from kivy.properties import DictProperty, ListProperty, ObjectProperty
from kivy.lang import Builder
from kivy.clock import mainthread

from kivymd.uix.screenmanager import MDScreenManager


class LazyManager(MDScreenManager):
    """
    The LazyManager class inherits from kivymd.uix.screenmanager.MDScreenManager
    and adds lazy loading abilities to it.
    """

    # Dictionary to hold the raw views
    raw_views = DictProperty()

    # List to keep track of upstream views
    upstream_views = ListProperty()

    # Object to define the loading layout
    loading_layout = ObjectProperty()

    def __init__(self, *args, **kwargs):
        """
        Initialize the LazyManager and load the basic kvlang files.
        """
        super(LazyManager, self).__init__(*args, **kwargs)
        self._load_basic_kvlang_files()

    def switch(self, name_screen: str, preload: bool = False, *args) -> None:
        """
        Switch to the specified screen. If the screen is not already loaded, it loads the
        screen dynamically and adds it to the screen manager.

        :param name_screen: The name of the screen to switch to.
        :param preload: If True, preloads the screen without switching immediately.
        """

        @mainthread
        def switch(*args) -> None:
            """
            Switch the current screen to the specified screen on the main thread.
            """
            self.current = name_screen
            self.dismiss_loader()

        if not self.has_screen(name_screen):
            module = self.raw_views[name_screen]["module"]
            self._load_kvlang_file(module)
            
            # Create the screen view and add it to the screen manager
            view = self.raw_views[name_screen]['object']()
            view.name = name_screen
            view.manager_screens = self
            
            self.add_widget(view)
            self.upstream_views.extend(name_screen)

        if not preload:
            # Show the loading layout while the screen is being loaded
            self.start_loader()
            switch()

    def start_loader(self, *args) -> None:
        """
        Display the loading layout on the current screen.
        """
        self.loader_screen = self.current_screen
        self.loader_screen.add_widget(self.loading_layout)
        self.loading_layout.display()

    def dismiss_loader(self, *args) -> None:
        """
        Remove the loading layout from the current screen.
        """
        self.loader_screen.remove_widget(self.loading_layout)
        self.loading_layout.dismiss()

    def _load_basic_kvlang_files(self, *args) -> None:
        """
        Load the basic kvlang files required for global components and base screens.
        """
        global_components_filepath = os.path.join("View", "components", "**", "*.kv")
        for filepath in glob.glob(global_components_filepath, recursive=True):
            Builder.load_file(filepath)

        base_screen_filepath = os.path.join("View", "*.kv")
        for filepath in glob.glob(base_screen_filepath, recursive=True):
            Builder.load_file(filepath)

    def _load_kvlang_file(self, module: str, *args) -> None:
        """
        Load the kvlang files dynamically based on the module path.

        :param module: The module path to convert to a kvlang file path.
        """
        dynamic_filepath = os.path.join(module.replace(".", os.sep), "**", "*.kv")
        for filepath in glob.glob(dynamic_filepath, recursive=True):
            Builder.load_file(filepath)
