from kivy.uix.widget import Widget
from kivy.graphics.instructions import Image
from kivy.graphics import Rectangle
from kivy.graphics.texture import Texture
from kivy.graphics import BorderImage
from kivy.graphics import Color

import numpy as np
import sys

from Decorators import Debugger


class Drawer(Widget):
    def __init__(self, map_size: int = 32, **kwargs):
        super().__init__(**kwargs)
        self.map_size: int = map_size

        # Binds
        self.bind(size=self.renderCanvas)
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
        self.colorMapBuffer = {0: [(200, 200, 200), (220, 220, 220)],
                               2: [(174, 136, 188), (184, 146, 198)],
                               1: [(207, 134, 115), (217, 144, 125)]}

        # Brush Properties
        self.brushColor = 1
        self.brushSize = 4
        self.tileSize = 0
        self.touch = [-1, -1]

        # Mouse states
        self.pressed = False
        self.lastPos = [-1, -1]

        # Sim states
        self.time_between_steps = 100

        # Data
        self.data = np.random.randint(3, size=(self.map_size, self.map_size))
        self.left_corner = [0, 0]
        self.texture = Texture.create(size=(self.map_size, self.map_size))
        with self.canvas:
            Color(1, 1, 1, 1)
            self.rectangle = Rectangle(size=self.size,
                                       texture=self.texture)
        self.drawCount = 0

    def __update_location_properties(self):
        """Eval the optimal size of tile and leftCorner pos"""
        print('Updating location properties:'
              f'Rows\\Cols = {self.map_size, self.map_size}')
        sizeX = self.size[0] / self.map_size
        sizeY = self.size[1] / self.map_size

        if sizeX > sizeY:
            self.tileSize = sizeY
        else:
            self.tileSize = sizeX

        self.left_corner = [10 + (self.size[0] - self.tileSize * self.map_size) / 2,
                            10 + (self.size[1] - self.tileSize * self.map_size) / 2]
        print(f'Updating finished:Left Corner: {self.left_corner}, Tile Size: {self.tileSize}')

    def buf_from_matrix(self):
        buf = np.array([bytes(self.colorMapBuffer[data][(i + j) % 2]) for (i, j), data in np.ndenumerate(self.data)]) \
            .ravel()
        buf = b''.join(buf)
        return buf

    def __update_texture(self):
        # FIXME: Normal texture creation
        self.texture = Texture.create(size=(self.map_size, self.map_size))

        self.texture.blit_buffer(self.buf_from_matrix(), colorfmt='rgb', bufferfmt='ubyte')
        self.texture.mag_filter = 'nearest'
        self.texture.min_filter = 'nearest'

    def renderCanvas(self, *args, **kwargs):
        self.drawCount += 1
        print(f'Draw count: {self.drawCount}')
        self.__update_location_properties()
        self.__update_texture()
        self.rectangle.size = [self.tileSize * self.map_size, self.tileSize * self.map_size]
        self.rectangle.pos = self.left_corner
        self.rectangle.texture = self.texture

        # with self.canvas:
        #     Color(1, 1, 1, 1)
        #
        #     self.rectangle = Rectangle(size=[self.tileSize * self.map_size,
        #                                      self.tileSize * self.map_size],
        #                                texture=self.texture,
        #                                pos=self.left_corner)

        print(f'Drawing with properties:\n'
              f'Row\\Cols:{self.map_size, self.map_size}\n'
              f'Size ={self.rectangle.size}\n'
              f'Pos = {self.rectangle.pos}\n')

    def _brush_area(self, touch):
        x, y = touch
        left = 0 if (x - self.brushSize + 1) < 0 else (x - self.brushSize + 1)
        right = self.width if (x + self.brushSize) > self.width else (x + self.brushSize)
        up = self.height if (y + self.brushSize) > self.height else (y + self.brushSize)
        down = 0 if (y - self.brushSize + 1) < 0 else (y - self.brushSize + 1)
        self.data[down:up, left:right] = self.brushColor

    def on_touch_down(self, touch):
        self.pressed = True

    def on_touch_up(self, touch):
        self.pressed = False
        self.lastPos = [-1, -1]

    def on_touch_move(self, touch):
        if [0, 0] > [touch.x, touch.y] > self.size:
            return
        i: int = int((touch.x - self.left_corner[0]) / self.tileSize)
        j: int = int((touch.y - self.left_corner[1]) / self.tileSize)
        if [i, j] == self.touch:
            return
        self.__update_location_properties()
        self.touch = [i, j]
        print(f'TileCords:{i}, {j}')
        self._brush_area([i, j])
        self.renderCanvas()

    def clearCanvas(self):
        self.data = np.zeros((self.map_size, self.map_size))
        self.renderCanvas()