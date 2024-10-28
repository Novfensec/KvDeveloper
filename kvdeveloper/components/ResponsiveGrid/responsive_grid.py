from kivy.properties import NumericProperty
from kivymd.uix.gridlayout import MDGridLayout


class ResponsiveGrid(MDGridLayout):

    max_cols = NumericProperty(4)
    """
    Maximum number of columns in the grid.
    """

    min_cols = NumericProperty(1)
    """
    Minimum number of columns in the grid.
    """

    scale_width = NumericProperty(35)
    """
    Width of a single element.
    """

    def __init__(self, *args, **kwargs):
        super(ResponsiveGrid, self).__init__(*args, **kwargs)
        self.bind(size=self.adjust_cols)

    def adjust_cols(self, *args):
        width, height = self.size

        for x in range(self.min_cols, -~self.max_cols):
            if (self.scale_width * x) < width < (self.scale_width * (x + 1)):
                self.cols = x
                break
