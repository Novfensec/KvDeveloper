from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.uix.widget import Widget
from kivymd.uix.card import MDCard


class ITDCard(MDCard):

    title = StringProperty()
    """
    Title for the Card.
    """

    desc = StringProperty()
    """
    Description for the card.
    """

    source = StringProperty()
    """
    Image path.
    """

    image_height = NumericProperty()
    """
    Image Height.
    """

    image_ratio = ListProperty([4, 3])
    """
    Image Aspect ratio.
    """

    def __init__(self, *args, **kwargs):
        super(ITDCard, self).__init__(*args, **kwargs)
        self.bind(size=self.adjust_image_size)

    def adjust_image_size(self, *args) -> None:
        w_ratio, h_ratio = self.image_ratio
        self.image_height = h_ratio / w_ratio * self.width
