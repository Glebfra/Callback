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

class MyApp(MDApp):
    def __init__(self, width=4, height=4, excitation_time=3, refractory_time=5, critical_value=1,
                 activator_remain=0.55, **kwargs):
        super().__init__(**kwargs)
        self.drawer = Drawer()
        self.theme_cls = ThemeManager()
        Builder.load_file('fig.kv')
        self.container = Container()
        self.drawer = self.container.ids.Drawer
        self.state = State(width=width,
                           height=height,
                           excitation_time=excitation_time,
                           refractory_time=refractory_time,
                           critical_value=critical_value,
                           activator_remain=activator_remain
                           )

    def build(self):
        self.drawer.bind(on_touch_down=self.on_touch_down)
        self.drawer.bind(on_touch_move=self.on_touch_move)
        self.drawer.bind(on_touch_up=self.on_touch_up)

        Window.bind(on_draw=self.on_draw)

        self.container.ids.row.text = str(self.state.width)
        self.container.ids.column.text = str(self.state.height)
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

    def on_draw(self, instance):
        self.renderCanvas()

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
        self.renderCanvas()
        self.drawer.lastPos = [-1, -1]

    def check_resize(self, instance, x, y):
        self.renderCanvas()

    def resizeBrush(self, instance):
        self.drawer.brushSize = instance.value

    def TF_changeWidth(self, ins):
        width = int(ins.text)
        if width > 32:
            width = 32
        if width < 1:
            width = 1
        self.state.states = np.zeros(shape=(self.state.width, self.state.height))
        self.renderCanvas()

    def TF_changeHeight(self, ins):
        try:
            height = eval(ins.text)
        except:
            ins.text = '1'
            height = eval(ins.text)
        if height > 32:
            height = 32
        if height < 1:
            height = 1
        ins.text = str(height)
        self.state.height = height
        self.state.states = np.zeros(shape=(self.state.width, self.state.height))

        self.renderCanvas()

    def on_touch_down(self, instance, touch):
        # TODO: Draw the border while moving mouse
        self.drawer.pressed = True

        # [i, j] - coords of selected tile
        i: int = int((touch.x - self.drawer.left_corner[0]) / self.drawer.tileSize)
        j: int = int((touch.y - self.drawer.left_corner[1]) / self.drawer.tileSize)

        print(f'pos:[{i},{j}] on [{touch.x},{touch.y}]')
        # Eval the area to brush
        left = 0 if i - self.drawer.brushSize + 1 < 0 else i - self.drawer.brushSize + 1
        right = self.state.width if i + self.drawer.brushSize > self.state.width else i + self.drawer.brushSize
        down = 0 if j - self.drawer.brushSize + 1 < 0 else j - self.drawer.brushSize + 1
        up = self.state.height if j + self.drawer.brushSize > self.state.height else j + self.drawer.brushSize

        # Eval the properties of selection
        self.drawer.sel_pos = [self.drawer.left_corner[0] + left * self.drawer.tileSize,
                               self.drawer.left_corner[1] + down * self.drawer.tileSize]
        self.drawer.sel_size = [self.drawer.tileSize * (right - left), self.drawer.tileSize * (up - down)]

        if (0 <= i < self.state.width) and \
                (0 <= j < self.state.height) and \
                (self.drawer.lastPos != [i, j]) and \
                (self.state.states[i, j] != self.drawer.brushColor or self.drawer.brushSize != 1):
            states = self.state.states
            states[left:right, down:up] = self.drawer.brushColor
            self.state.states = states
            self.drawer.lastPos = [i, j]
            self.renderCanvas()

    def on_touch_move(self, ins, touch):
        self.on_touch_down(ins, touch)

    def on_touch_up(self, instance, touch):
        self.drawer.pressed = False
        self.drawer.lastPos = [-1, -1]
        self.renderCanvas()

    def btn_nextStep(self, ins):
        self.state.next_step()
        self.renderCanvas()

    def renderCanvas(self):
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
        # Redrawing the canvas
        with self.drawer.canvas:
            # Drawing the selection
            if self.drawer.pressed:
                color = self.drawer.colorMap[self.drawer.brushColor]
                Color(color[0], color[1], color[2], color[3])
                Rectangle(Color=self.drawer.colorMap[self.drawer.brushColor],
                          size=self.drawer.sel_size,
                          pos=self.drawer.sel_pos)
            # Drawing tiles
            Color(1, 1, 1)
            for i in range(self.state.width):
                for j in range(self.state.height):
                    BorderImage(source=self.drawer.iconMap[self.state.states[i,j]],
                                size=(self.drawer.tileSize, self.drawer.tileSize),
                                border=(0, 0, 0, 0),
                                pos=(self.drawer.left_corner[0] + self.drawer.tileSize * i,
                                     self.drawer.left_corner[1] + self.drawer.tileSize * j))
            # TODO: Make color of icons depend on states value


    def TF_change_refactory_time(self,instance):
        pass


