from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.behaviors.state_layer_behavior import StateLayerBehavior
from kivy.properties import OptionProperty


class Container(MDBoxLayout, StateLayerBehavior):
    type = OptionProperty(
        "fluid",
        options=("fluid", "small", "medium", "large"),
    )

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = [10, 5, 10, 5]
        self.bind(type=self.adjust_size)
        self.adaptive_height = True
        self.spacing = "10dp"

    def adjust_size(self, *args) -> None:
        if self.parent:
            if self.type == "small":
                self.padding = [self.width * 0.9, 5, self.width * 0.9, 5]
            elif self.type == "medium":
                self.padding = [self.width * 0.6, 5, self.width * 0.6, 5]
            elif self.type == "large":
                self.padding = [self.width * 0.3, 5, self.width * 0.3, 5]
            elif self.type == "fluid":
                pass
