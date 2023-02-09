import sys, os

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
from kivy.uix.label import Label

from Backend.Calculations import Calculations
from FrontEnd.Container import Container, LoadDialog, SaveDialog
from FrontEnd.Drawer import Drawer
from kivy.graphics.texture import Texture
from config import *

from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window, Config
import json

import numpy as np


class MyApp(MDApp):
    Config.set('input', 'mouse', 'mouse,disable_multitouch')

    Factory.register('Root', cls=Container)
    Factory.register('LoadDialog', cls=LoadDialog)
    Factory.register('SaveDialog', cls=SaveDialog)

    def __init__(self, size=32, h=3, g=0.4, refraction_time=7, arousal_time=5, background_logic=1, **kwargs):
        super().__init__(**kwargs)

        Builder.load_file('fig.kv')
        self.container = Container()

        self.drawer = self.container.ids.Drawer
        self.drawer.map_size = size
        self.drawer.data = np.zeros((size, size))

        self.drawer.bind(on_touch_down=self.on_touching_down)
        self.drawer.bind(on_touch_up=self.on_touching_up)
        self.drawer.bind(on_touch_move=self.on_touching_move)

        self.calculations = Calculations(number_of_partitions=size,
                                         h=h,
                                         g=g,
                                         refraction_time=refraction_time,
                                         arousal_time=arousal_time,
                                         background_logic=1,
                                         )
        self.renderCanvas()
        self.drawer.on_resize()
        Window.size = (1100,600)

    def open_settings(self, *largs):
        pass
    def build(self):
        self.updateFields()

        self.theme_cls.theme_style = 'Light'
        self.theme_cls.material_style = "M3"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Blue"
        return self.container

    def button_press(self, ins):
        IDS = self.container.ids
        if ins == IDS.brush_plus:
            self.drawer.brushColor += 1
            IDS.cell_phase.text = str(self.drawer.brushColor)
            print('brush +')
        elif ins == IDS.brush_minus:
            self.drawer.brushColor -= 1
            if self.drawer.brushColor < 0:
                self.drawer.brushColor = 0
            IDS.cell_phase.text = str(self.drawer.brushColor)
            print('brush -')
        elif ins == IDS.size_plus:
            self.drawer.brushSize += 1
            IDS.brush_size.text = str(self.drawer.brushSize)
            print('size +')
        elif ins == IDS.size_minus:
            self.drawer.brushSize -= 1
            if self.drawer.brushSize < 1:
                self.drawer.brushSize = 1
            IDS.brush_size.text = str(self.drawer.brushSize)
            print('size -')
        elif ins == IDS.period_plus:
            self.drawer.period += 1
            IDS.period.text = str(self.drawer.period)
            print('period +')
        elif ins == IDS.period_minus:
            self.drawer.period -= 1
            if self.drawer.brushSize < 1:
                self.drawer.brushSize = 1
            IDS.period.text = str(self.drawer.period)
            print('period -')

    def bth_change_color(self, instance):
        self.drawer.brushColor = int(instance.text)
        self.drawer.oldPos = [-1, -1]
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
            if not (CANVAS_MIN_SIZE <= value <= CANVAS_MAX_SIZE):
                ins.text = str(self.calculations.number_of_partitions)
                return
            self.calculations.changing_the_size_of_matrices(value)
            self.drawer.data = self.calculations.matrix_of_states
            self.drawer.map_size = self.calculations.number_of_partitions
            self.renderCanvas()

        elif ins == IDS.refractory_time:
            if value <= 0:
                ins.text = str(self.calculations.refraction_time)
                return
            self.calculations.refraction_time = value

        elif ins == IDS.excitation_time:
            if value <= 0:
                ins.text = str(self.calculations.arousal_time)
                return
            self.calculations.arousal_time = value

        elif ins == IDS.activator_remain:
            if not (0 <= value <= 1):
                ins.text = str(self.calculations.g)
                return
            self.calculations.g = value

        elif ins == IDS.critical_value:
            if value < 0:
                ins.text = str(self.calculations.h)
                return
            self.calculations.h = value

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
        elif ins == IDS.period:
            self.drawer.period = int(ins.text)

    def create_state_from_file(self, filepath):
        with open(filepath, 'r') as file:
            properties = json.load(file)
        return Calculations(**properties)

    def loadState(self, ins):  # FIXME: Чини
        ins.line_color_normal = (0, 0, 0, 0.38)
        self.calculations = self.create_state_from_file(ins.text)

        self.updateFields()
        self.container.ids.FilePath.icon_right = 'file-document-check-outline'
        self.drawer.data = self.calculations.matrix_of_states
        self.drawer.map_size = self.calculations.number_of_partitions
        self.renderCanvas()
        print('loading State')
        # self.container.ids.FilePath.icon_right = 'file-document-remove-outline'
        # ins.line_color_normal = (1, 0, 0, 1)

    def saveState(self, path, filename):
        output = {'number_of_partitions': self.calculations.number_of_partitions,
                  'h': self.calculations.h,
                  'g': self.calculations.g,
                  'refraction_time': self.calculations.refraction_time,
                  'arousal_time': self.calculations.arousal_time,
                  'background_logic': self.calculations.background_logic,
                  'logic_of_boundary_conditions': self.calculations.logic_of_boundary_conditions,
                  'matrix_of_states': self.calculations.matrix_of_states.tolist()
                  }
        with open(f'{os.path.join(path, filename)}.json', 'w') as stream:
            json.dump(output, stream)
        self.container.dismiss_popup()

    def updateFields(self):
        self.container.ids.refractory_time.text = str(self.calculations.refraction_time)
        self.container.ids.excitation_time.text = str(self.calculations.arousal_time)
        self.container.ids.activator_remain.text = str(self.calculations.g)
        self.container.ids.critical_value.text = str(self.calculations.h)
        self.container.ids.time_between_steps.text = str(self.drawer.time_between_steps)

        self.container.ids.size.text = str(self.calculations.number_of_partitions)

        self.container.ids.brush_size.text = str(self.drawer.brushSize)
        self.container.ids.cell_phase.text = str(self.drawer.brushColor)
        self.container.ids.period.text = str(self.drawer.period)

    def play_button_press(self, ins):
        if ins.icon == 'play':
            ins.icon = 'stop'
            ins.icon_color = [1, 0, 0, 1]
            self.loopEvent = Clock.schedule_interval(self.worker, self.drawer.time_between_steps / 1000)
        else:
            ins.icon = 'play'
            ins.icon_color = [.2, .8, .2, 1]
            Clock.unschedule(self.loopEvent)

    def next_step_button_press(self):
        print(self.container.size)
        self.calculations.calculation_step()
        self.drawer.data = self.calculations.matrix_of_states
        self.renderCanvas()

    def worker(self, period):
        self.calculations.calculation_step()
        self.drawer.data = self.calculations.matrix_of_states
        self.renderCanvas()

    def create_peacemaker(self, i, j, period):
        self.drawer.update_location_properties()
        label = Label(color=(0, 0, 0, 1),
                      text=str(period))
        label._label.refresh()
        label._label.texture.mag_filter = 'nearest'
        label._label.texture.min_filter = 'nearest'

        self.calculations.matrix_of_periods[i, j] = period
        if (i, j) in self.drawer.peacemakers:
            self.drawer.peacemakers[(i, j)].texture = label._label.texture
            self.drawer.peacemakers[(i, j)].size = (label._label.texture.size[0] /
                                                    label._label.texture.size[
                                                        1] * self.drawer.tileSize, self.drawer.tileSize)
            self.drawer.peacemakers[(i, j)].pos = (self.drawer.tileSize * j + self.drawer.left_corner[0],
                                                   self.drawer.tileSize * i + self.drawer.left_corner[1])
        else:
            with self.drawer.canvas:
                Color(1, 1, 1, 1)
                self.drawer.peacemakers[(i, j)] = Rectangle(size=(label._label.texture.size[0] /
                                                                  label._label.texture.size[
                                                                      1] * self.drawer.tileSize, self.drawer.tileSize),
                                                            pos=(self.drawer.tileSize * j + self.drawer.left_corner[0],
                                                                 self.drawer.tileSize * i + self.drawer.left_corner[1]),
                                                            texture=label._label.texture)
                print(f"Create text with size:{self.drawer.peacemakers[(i, j)].size}"
                      f"pos:{self.drawer.peacemakers[(i, j)].pos}")

    def renderCanvas(self, *args, **kwargs):
        self.drawer.update_location_properties()
        self.drawer.update_texture()
        self.drawer.rectangle.texture = self.drawer.texture

        # my_label = Label()
        # my_label.text = '123'
        # my_label.color = (0,0,0)
        # my_label._label.refresh()
        #
        # my_label._label.texture.mag_filter = 'nearest'
        # my_label._label.texture.min_filter = 'nearest'
        # with self.drawer.canvas:
        #     Color(1,1,1,1)
        #     Rectangle(size=(self.drawer.tileSize,my_label._label.texture.size[1]/my_label._label.texture.size[0]*self.drawer.tileSize),
        #               pos=(self.drawer.tileSize*3+self.drawer.left_corner[0],
        #                    self.drawer.tileSize*10+self.drawer.left_corner[1]),
        #               texture=my_label._label.texture)

    def brush_area(self, touch,button):
        x, y = touch
        left = 0 if (x - self.drawer.brushSize + 1) < 0 else (x - self.drawer.brushSize + 1)
        right = self.drawer.map_size if (x + self.drawer.brushSize) > self.drawer.map_size else (
                x + self.drawer.brushSize)
        up = self.drawer.map_size if (y + self.drawer.brushSize) > self.drawer.map_size else (y + self.drawer.brushSize)
        down = 0 if (y - self.drawer.brushSize + 1) < 0 else (y - self.drawer.brushSize + 1)

        if button == 'right':
            for i in range(left,right):
                for j in range(down,up):
                    self.create_peacemaker(j, i, self.drawer.period)
        elif button == 'left':
            self.drawer.data[down:up, left:right] = self.drawer.brushColor
            self.calculations.matrix_of_states[down:up, left:right] = self.drawer.brushColor
            self.calculations.updateCalcs()

    def on_touching_down(self, ins, touch):
        self.on_touching_move(ins, touch)
        self.pressed = True

    def on_touching_up(self, touch, ins):
        self.pressed = False
        self.lastPos = [-1, -1]

    def on_touching_move(self, ins, touch):
        print(touch.button)
        if [0, 0] > [touch.x, touch.y] > self.size:
            return
        i: int = int((touch.x - self.drawer.left_corner[0]) / self.drawer.tileSize)
        j: int = int((touch.y - self.drawer.left_corner[1]) / self.drawer.tileSize)
        self.drawer.update_location_properties()
        self.brush_area([i, j],touch.button)
        self.renderCanvas()

    def clearCanvas(self):
        self.drawer.data = np.zeros((self.calculations.number_of_partitions, self.calculations.number_of_partitions))
        self.calculations.matrix_of_states = np.zeros(
            (self.calculations.number_of_partitions, self.calculations.number_of_partitions))  # Матрица состояний
        self.calculations.phase_matrix = np.zeros(
            (self.calculations.number_of_partitions, self.calculations.number_of_partitions))  # Матрица фаз
        self.calculations.production_matrix = np.zeros(
            (self.calculations.number_of_partitions, self.calculations.number_of_partitions))  # Матр производства
        self.calculations.concentration_matrix = np.zeros(
            (self.calculations.number_of_partitions, self.calculations.number_of_partitions))  # Матр конц
        self.calculations.matrix_of_periods = np.zeros(
            (self.calculations.number_of_partitions, self.calculations.number_of_partitions))  # Матр периодов
        self.calculations.time_matrix = np.zeros(
            (self.calculations.number_of_partitions, self.calculations.number_of_partitions))  # Матр времени
        for key,value in self.drawer.peacemakers.items():
            self.drawer.peacemakers[key].size = (0, 0)
        self.drawer.peacemakers = {}
        self.drawer.on_resize()
        self.renderCanvas()


    def change_background(self, ins):
        IDS = self.container.ids
        if ins == IDS.moore:
            IDS.drop_item.text = "Moore background"
