from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.behaviors.state_layer_behavior import StateLayerBehavior
from kivy.properties import OptionProperty


class Container(MDBoxLayout, StateLayerBehavior):
    type = OptionProperty(
        "fluid",
        options=("fluid", "small", "medium", "large"),
    )
    """
    The type of the conatiner.  
    """

    def __init__(self, *args, **kwargs):
        super(Container, self).__init__(*args, **kwargs)
        self.bind(size=self.adjust_size)

    def adjust_size(self, *args) -> None:
        if self.parent:
            if self.type == "small":
                self.padding = [self.width * 0.08, 10, self.width * 0.08, 10]
            elif self.type == "medium":
                self.padding = [self.width * 0.04, 10, self.width * 0.04, 10]
            elif self.type == "large":
                self.padding = [self.width * 0.01, 10, self.width * 0.01, 10]
            elif self.type == "fluid":
                pass
