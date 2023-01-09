
from kivy.uix.widget import Widget
from kivy.graphics.instructions import Image
from kivy.graphics import Rectangle

class Drawer(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Data
        self.figures = None

        self.selection = Rectangle(pos=[0,0], size=[0,0])
        self.canvas.add(self.selection)

        # Maps
        self.textureMap = {0: Image('FrontEnd\\Icons\\calm.png').texture,
                           1: Image('FrontEnd\\Icons\\chill.png').texture,
                           2: Image('FrontEnd\\Icons\\angry.png').texture}


        self.iconMap = {0: 'FrontEnd\\Icons\\calm.png',
                        1: 'FrontEnd\\Icons\\chill.png',
                        2: 'FrontEnd\\Icons\\angry.png'}
        self.colorMap = {0: (.84, .80, .66, .5),
                         1: (.68, .53, .74, .5),
                         2: (.81, .53, .45, .5)}

        # Array properties
        self.rows_count = 20
        self.cols_count = 20
        self.left_corner = None  # Coords of left-bottom corner on drawing

        # Selection properties
        self.sel_size = [0, 0]
        self.sel_pos = [0, 0]

        # Brush Properties
        self.brushColor = 1
        self.brushSize = 1
        self.tileSize = 0

        # Mouse states
        self.pressed = False
        self.lastPos = [-1, -1]

        # Sim states
        self.time_between_steps = 100

