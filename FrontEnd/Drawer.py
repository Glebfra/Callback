import numpy as np
from kivy.graphics import Color, BorderImage
from kivy.uix.widget import Widget


class Drawer(Widget):

    def __init__(self, **kwargs):
        # self.fig = plt.figure()
        # self.ax = self.fig.add_subplot()
        super().__init__(**kwargs)
        self.leftCorner = None
        self.brushColor = 2
        self.brushSize = 1
        self.iconMap = {0: 'FrontEnd\\Icons\\calm.png',
                        1: 'FrontEnd\\Icons\\chill.png',
                        2: 'FrontEnd\\Icons\\angry.png'}
        self.rowsCount = 20
        self.colsCount = 20
        self.Corner = [0, 0]
        self.Data = np.zeros(shape=(self.rowsCount, self.colsCount))
        self.tileSize = 0
        self.figures = [[0 for x in range(self.colsCount)] for y in range(self.rowsCount)]
        self.lastPos = [-1, -1]

    def on_touch_down(self, touch):
        i = int((touch.x - self.leftCorner[0]) / self.tileSize)
        j = int((touch.y - self.leftCorner[1]) / self.tileSize)

        print(f'x: {i}, y: {j}')
        if (i < 0) or (j < 0) or self.lastPos == [i, j] or self.Data[i, j] == self.brushColor:
            return
        try:
            self.Data[i, j] = self.brushColor
            print(f'Drawing on color {self.brushColor}')
            self.lastPos = [i, j]
            self.drawCanvas()
        except:
            pass

    def on_touch_move(self, touch):
        self.on_touch_down(touch)

    def drawCanvas(self):
        sizeX = self.size[0] / self.rowsCount
        sizeY = self.size[1] / self.colsCount
        if sizeX > sizeY:
            self.tileSize = sizeY
        else:
            self.tileSize = sizeX

        self.leftCorner = [10 + (self.size[0] - self.tileSize * self.rowsCount) / 2,
                           10 + (self.size[1] - self.tileSize * self.colsCount) / 2]
        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 1)
            for i in range(self.rowsCount):
                for j in range(self.colsCount):
                    (self.figures[i][j]) = BorderImage(source=self.iconMap[self.Data[i, j]],
                                                       size=(self.tileSize, self.tileSize),
                                                       border=(1, 1, 1, 1),
                                                       pos=(self.leftCorner[0] + self.tileSize * i,
                                                            self.leftCorner[1] + self.tileSize * j))
