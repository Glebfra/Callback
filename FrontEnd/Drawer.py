from . import *

import matplotlib.pyplot as plt
import numpy as np
class Drawer():
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.brushColor = 2
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot()
        self.mousePressed = False
        self.oldPos = [-1, -1]

        self.ax.set_xticks(np.linspace(0.5, 100.5, 101))
        self.ax.set_yticks(np.linspace(0.5, 100.5, 101))

        self.ax.axis('off')
        self.ax.grid('on')

        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.fig.canvas.mpl_connect('button_release_event', self.release)
        self.fig.canvas.mpl_connect('motion_notify_event', self.motion)

        self.Data = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0],
                              [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0],
                              [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                              [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0],
                              [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0],
                              [0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
                              [0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 0, 2, 2, 0],
                              [0, 2, 0, 0, 0, 0, 1, 1, 0, 0, 2, 0, 0, 2, 0],
                              [0, 2, 0, 0, 0, 0, 1, 0, 1, 0, 2, 2, 2, 2, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
        self.image = plt.imshow(X=self.Data)

    def onclick(self, event):
        self.mousePressed = True
        self.motion(event)

    def release(self, event):
        self.mousePressed = False

    def motion(self, event):
        try:
            x = int(event.xdata + 1 / 2)
            y = int(event.ydata + 1 / 2)
            if self.mousePressed and ([x, y] != self.oldPos):
                self.oldPos = [x, y]
                self.Data[y, x] = self.brushColor
                self.image.set_data(self.Data)
                self.fig.canvas.draw_idle()
        except:
            pass
