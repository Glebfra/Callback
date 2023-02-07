import sys

from kivy.graphics import Color, BorderImage, Rectangle

from kivy.lang.builder import Builder
from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivy.factory import Factory
from kivy.clock import Clock, _default_time as time  # ok, no better way to use the same clock as kivy, hmm
from kivy.properties import ListProperty
from threading import Thread
from time import sleep
from time import perf_counter

from Backend.State import State
from FrontEnd.Container import Container, LoadDialog, SaveDialog, ConfirmDialog
from FrontEnd.Drawer import Drawer
from kivy.graphics.texture import Texture
from config import *

from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout

import numpy as np

class MyApp(MDApp):
    Factory.register('Root', cls=Container)
    Factory.register('LoadDialog', cls=LoadDialog)
    Factory.register('SaveDialog', cls=SaveDialog)
    Factory.register('ConfirmDialog', cls=ConfirmDialog)


    def __init__(self, size=32, excitation_time=3, refractory_time=5, critical_value=1,
                 activator_remain=0.55, **kwargs):
        super().__init__(**kwargs)

        Builder.load_file('fig.kv')
        self.container = Container()

        self.drawer = self.container.ids.Drawer
        self.drawer.map_size = size
        self.drawer.data = np.zeros((size,size))

        self.state = State(width=size,
                           height=size,
                           excitation_time=excitation_time,
                           refractory_time=refractory_time,
                           critical_value=critical_value,
                           activator_remain=activator_remain
                           )

    def build(self):
        self.updateFields()

        self.theme_cls.theme_style = 'Light'
        self.theme_cls.material_style = "M3"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Blue"

        return self.container

    def bth_change_color(self, instance):
        self.drawer.brushColor = int(instance.text)
        self.drawer.oldPos = [-1, -1]
        print(f'color changed to {self.drawer.brushColor}')
        self.drawer.lastPos = [-1, -1]
        with self.drawer.canvas:
            color = self.drawer.colorMap[self.drawer.brushColor]
            Color(color[0], color[1], color[2], color[3])
            self.drawer.selection = Rectangle(pos=[0, 0], size=[0, 0])

    def resizeBrush(self, instance):
        instance.value = int(instance.value)
        self.drawer.brushSize = round(instance.value)

    def textfield_change(self, ins):
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
        if ins == IDS.size:
            print('changing map size')
            if not (CANVAS_MIN_SIZE <= value <= CANVAS_MAX_SIZE):
                ins.text = str(self.state.width)
                return
            self.state.resize_states(value, value)
            self.drawer.data = self.state.states
            self.drawer.map_size = self.state.width
            self.drawer.renderCanvas()

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
            if not (0 <= value <= 1):
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
                ins.text = str(self.drawer.time_between_steps)
                return
            self.drawer.time_between_steps = value
        elif ins == IDS.brush_size:
            if value < 0:
                ins.text = str(self.drawer.brushSize)
                return
            self.drawer.brushSize = value
        elif ins == IDS.cell_phase:
            if value < 0:
                ins.text = str(self.drawer.brushColor)
                return
            self.drawer.brushColor = value
        else:
            print('Warning:Cant find the id')

    def loadState(self, ins):
        try:
            ins.line_color_normal = (0, 0, 0, 0.38)
            self.state = self.state.create_state_from_file(ins.text)
            self.updateFields()
            self.container.ids.FilePath.icon_right = 'file-document-check-outline'
            self.drawer.data = self.state.states
            self.drawer.map_size = self.state.width
            self.drawer.renderCanvas()
        except:
            self.container.ids.FilePath.icon_right = 'file-document-remove-outline'
            ins.line_color_normal = (1, 0, 0, 1)

    def updateFields(self):
        self.container.ids.refractory_time.text = str(self.state.refractory_time)
        self.container.ids.excitation_time.text = str(self.state.excitation_time)
        self.container.ids.activator_remain.text = str(self.state.activator_remain)
        self.container.ids.critical_value.text = str(self.state.critical_value)
        self.container.ids.time_between_steps.text = str(self.drawer.time_between_steps)

        self.container.ids.size.text = str(self.state.width)

    def play_button_press(self,ins):
        if ins.icon == 'play':
            ins.icon = 'stop'
            ins.icon_color = [1, 0, 0, 1]
            self.loopEvent = Clock.schedule_interval(self.worker, self.drawer.time_between_steps / 1000)
        else:
            ins.icon = 'play'
            ins.icon_color = [.2, .8, .2, 1]
            Clock.unschedule(self.loopEvent)

    def next_step_button_press(self):
        print('step')
        self.state.states = self.drawer.data
        self.state.next_step()
        self.drawer.data = self.state.states
        self.drawer.renderCanvas()
        np.set_printoptions(threshold=sys.maxsize)
        print(self.drawer.data)

    def worker(self, period):
        self.state.states = self.drawer.data
        self.state.next_step()
        self.drawer.data = self.state.states
        self.drawer.renderCanvas()
        print(f"FPS:{1 / period}")