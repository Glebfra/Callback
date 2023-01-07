import numpy as np
from kivy.core.window import Window
from kivy.graphics import Color, BorderImage, Rectangle
from kivy.lang.builder import Builder
from kivymd.app import MDApp
from kivymd.theming import ThemeManager

from Backend.State import State
from FrontEnd.Container import Container
from FrontEnd.Drawer import Drawer

from time import sleep
from config import *


class MyApp(MDApp):
    def __init__(self, width=4, height=4, excitation_time=3, refractory_time=5, critical_value=1,
                 activator_remain=0.55, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls = ThemeManager()
        Builder.load_file('fig.kv')
        self.container = Container()
        self.drawer = self.container.ids.Drawer

        self.drawer.bind(on_touch_down=self.on_touching_down)
        self.drawer.bind(on_touch_move=self.on_touching_down)
        self.drawer.bind(on_touch_up=self.on_touching_up)


        self.state = State(width=width,
                           height=height,
                           excitation_time=excitation_time,
                           refractory_time=refractory_time,
                           critical_value=critical_value,
                           activator_remain=activator_remain
                           )

    def build(self):

        self.container.ids.refractory_time.text = str(self.state.refractory_time)
        self.container.ids.excitation_time.text = str(self.state.excitation_time)
        self.container.ids.activator_remain.text = str(self.state.activator_remain)
        self.container.ids.critical_value.text = str(self.state.critical_value)
        self.container.ids.time_between_steps.text = str(self.drawer.time_between_steps)


        self.theme_cls.theme_style = 'Light'
        self.theme_cls.material_style = "M3"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Blue"

        return self.container

    def cont_on_motion(self, etype, me):
        print(me.profile)


    def btn_press(self, instance):
        if instance.icon == 'play':
            instance.icon = 'stop'
            instance.icon_color = [1, 0, 0, 1]
        else:
            instance.icon = 'play'
            instance.icon_color = [.2, .8, .2, 1]
        while True:
            print("Цикл")
            self.state.next_step()
            self.renderCanvas()
            sleep(1)

    def bth_change_color(self, instance):
        self.drawer.brushColor = int(instance.text)
        self.drawer.oldPos = [-1, -1]
        print(f'color changed to {self.drawer.brushColor}')
        self.drawer.lastPos = [-1, -1]

    def check_resize(self, instance, x, y):
        print('check resize')
        self.renderCanvas()

    def resizeBrush(self, instance):
        instance.value = int(instance.value)
        self.drawer.brushSize = instance.value

    def on_touching_down(self, instance, touch):
        if [0, 0] > [touch.x, touch.y] > instance.size:
            return
        # TODO: Draw the border while moving mouse
        self.drawer.pressed = True
        # [i, j] - coords of selected tile
        i: int = int((touch.x - self.drawer.left_corner[0]) / self.drawer.tileSize)
        j: int = int((touch.y - self.drawer.left_corner[1]) / self.drawer.tileSize)
        self.paintCanvas(i, j)


    def on_touching_up(self, instance, touch):
        self.drawer.pressed = False
        self.drawer.lastPos = [-1, -1]


    def btn_nextStep(self, ins):
        self.state.next_step()
        self.renderCanvas()

    def paintCanvas(self, i, j):
        # Eval the area to brush
        left = 0 if i - self.drawer.brushSize + 1 < 0 else i - self.drawer.brushSize + 1
        right = self.state.width if i + self.drawer.brushSize > self.state.width else i + self.drawer.brushSize
        down = 0 if j - self.drawer.brushSize + 1 < 0 else j - self.drawer.brushSize + 1
        up = self.state.height if j + self.drawer.brushSize > self.state.height else j + self.drawer.brushSize
        if (0 <= i < self.state.width) and \
                (0 <= j < self.state.height) and \
                (self.drawer.lastPos != [i, j]) and \
                (self.state.states[i, j] != self.drawer.brushColor or self.drawer.brushSize != 1):

            states = self.state.states
            states[left:right, down:up] = self.drawer.brushColor
            self.state.states = states

            for i in range(left,right):
                for j in range(down,up):
                    self.drawer.figures[i][j].texture = self.drawer.textureMap[self.drawer.brushColor]

            self.drawer.lastPos = [i, j]
            print('Brushing...')

    def renderCanvas(self, *args):
        # Eval the optimal size of tile and leftCorner pos
        sizeX = self.drawer.size[0] / self.state.width
        sizeY = self.drawer.size[1] / self.state.height
        if sizeX > sizeY:
            self.drawer.tileSize = sizeY
        else:
            self.drawer.tileSize = sizeX
        self.drawer.left_corner = [10 + (self.drawer.size[0] - self.drawer.tileSize * self.state.width) / 2,
                                   10 + (self.drawer.size[1] - self.drawer.tileSize * self.state.height) / 2]

        # Clearing the canvas
        self.drawer.canvas.clear()
        self.drawer.figures = [[None for x in range(int(self.drawer.width))] for y in range(int(self.drawer.height))]
        # Redrawing the canvas
        with self.drawer.canvas:
            Color(1, 1, 1)
            # Drawing tiles
            for i in range(self.state.width):
                for j in range(self.state.height):
                    self.drawer.figures[i][j] = Rectangle(size=(self.drawer.tileSize, self.drawer.tileSize),
                                                          texture=self.drawer.textureMap[self.state.states[i, j]],
                                                          pos=(self.drawer.left_corner[0] + self.drawer.tileSize * i,
                                                               self.drawer.left_corner[1] + self.drawer.tileSize * j))
            # Drawing the selection
            if self.drawer.pressed:
                color = self.drawer.colorMap[self.drawer.brushColor]
                Color(color[0], color[1], color[2], color[3])
                Rectangle(Color=self.drawer.colorMap[self.drawer.brushColor],
                          size=self.drawer.sel_size,
                          pos=self.drawer.sel_pos)
            # TODO: Make color of icons depend on states value


    def TF_change(self, ins):
        if ins.text:
            try:
                value = int(ins.text)
            except:
                value = float(ins.text)
        else:
            ins.line_color_normal = (1, 0, 0, 1)
            return
        ins.line_color_normal = (0, 0, 0, 0.38)
        IDS = self.container.ids
        if ins == IDS.row:
            print('changing rows count')
            if not (CANVAS_MIN_SIZE <= value <= CANVAS_MAX_SIZE):
                ins.text = str(self.state.width)
                return
            self.state.resize_states(value, self.state.height)
            self.renderCanvas()

        elif ins == IDS.column:
            print('changing cols count')
            if not (CANVAS_MIN_SIZE <= value <= CANVAS_MAX_SIZE):
                ins.text = str(self.state.height)
                return
            self.state.resize_states(self.state.width, value)
            self.renderCanvas()
            pass

        elif ins == IDS.refractory_time:
            if value <= 0:
                ins.text = str(self.state.refractory_time)
                return
            self.state.refractory_time = value

        elif ins == IDS.excitation_time:
            if value <= 0:
                ins.text = str(self.state.excitation_time)
                return
            self.state.excitation_time = value

        elif ins == IDS.activator_remain:
            if not (0 < value <= 1):
                ins.text = str(self.state.activator_remain)
                return
            self.state.activator_remain = value

        elif ins == IDS.critical_value:
            if value <= 1:
                ins.text = str(self.state.critical_value)
                return
            self.state.critical_value = value

        elif ins == IDS.time_between_steps:
            if value < 0:
                ins.text = str(self.state.time_between_steps)
                return
            self.state.time_between_steps = value
        else:
            print('Warning:Cant find the id')
