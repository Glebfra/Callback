import numpy as np
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivymd.uix.boxlayout import MDBoxLayout
from matplotlib import pyplot as plt
from matplotlib import ticker

from libs.garden.matplotlib import FigureCanvasKivyAgg

fig = plt.figure()
ax = fig.add_subplot()
ax.set_xticks(np.linspace(0.5, 14.5, 15))
ax.set_yticks(np.linspace(0.5, 14.5, 15))
ax.v

ax.grid('on')
test = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
ax_in = plt.imshow(cmap='binary',
                   X=test)

kp = False
def onclick(event):
    global kp
    kp = True

def release(event):
    global kp
    kp = False
def motion(event):
    global ax_in, fig, kp
    if kp:
        x = int(event.xdata + 1 / 2)
        y = int(event.ydata + 1 / 2)
        test[y][x] = 0
        ax_in.set_data(test)
        fig.canvas.draw_idle()


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


if __name__ == '__main__':
    MyApp().run()
