import numpy as np
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivymd.uix.boxlayout import MDBoxLayout
from matplotlib import pyplot as plt

from libs.garden.matplotlib import FigureCanvasKivyAgg

color = 2

fig = plt.figure()
ax = fig.add_subplot()

ax.set_xticks(np.linspace(0.5, 100.5, 101))
ax.set_yticks(np.linspace(0.5, 100.5, 101))
oldPos = [-1, -1]
ax.axis('off')
ax.grid('on')
test = [[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
test = np.zeros((48, 48), dtype=int)
test[1, 1]=2
ax_in = plt.imshow(X=test)

kp = False


def onclick(event):
    global kp
    kp = True
    motion(event)


def release(event):
    global kp
    kp = False


def motion(event):
    global ax_in, fig, kp, oldPos, color,  test
    try:
        x = int(event.xdata + 1 / 2)
        y = int(event.ydata + 1 / 2)

        if kp and ([x, y] != oldPos):
            oldPos = [x, y]
            test[y, x] = color
            ax_in.set_data(test)

            fig.canvas.draw_idle()
    except:
        pass


fig.canvas.mpl_connect('button_press_event', onclick)
fig.canvas.mpl_connect('button_release_event', release)
fig.canvas.mpl_connect('motion_notify_event', motion)


class Container(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        box_graph = self.ids.box_graph
        fig.subplots_adjust(left=0.01, bottom=0.01, right=.99, top=.99)
        box_graph.add_widget(FigureCanvasKivyAgg(plt.gcf()))


class MyApp(MDApp):
    theme_cls = ThemeManager()

    def build(self):
        Builder.load_file('fig.kv')
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.material_style = "M3"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Blue"
        theme_test = self.theme_cls.primary_color
        return Container()

    def btn_press(self, instance):
        if instance.icon == 'play':
            instance.icon = 'stop'

            instance.icon_color = [1, 0, 0, 1]
        else:
            instance.icon = 'play'
            instance.icon_color = [.2, .8, .2, 1]

    def bth_change_color(self, instance):
        global color, oldPos
        color = eval(instance.text)
        oldPos = [-1, -1]
        print(f'color changed to {color}')


if __name__ == '__main__':
    MyApp().run()
