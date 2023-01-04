from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.theming import ThemeManager

from Backend.State import State
from FrontEnd.Container import Container
from FrontEnd.Drawer import Drawer

class MyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls = ThemeManager()
        Builder.load_file('fig.kv')
        self.container = Container()
        self.drawer = self.container.ids.Drawer
        self.State = State(width=32,
                           height=32,
                           excitation_time=3,
                           refractory_time=5,
                           critical_value=1,
                           activator_remain=0.55
                           )

    def build(self):

        Window.bind(on_draw=self.on_draw)
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.material_style = "M3"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Blue"

        return self.container

    def on_draw(self,instance):
        self.drawer.drawCanvas()
    def btn_press(self, instance):
        if instance.icon == 'play':
            instance.icon = 'stop'
            instance.icon_color = [1, 0, 0, 1]
        else:
            instance.icon = 'play'
            instance.icon_color = [.2, .8, .2, 1]

    def bth_change_color(self, instance):
        self.drawer.brushColor = int(instance.text)
        self.drawer.oldPos = [-1, -1]
        print(f'color changed to {self.drawer.brushColor}')
        self.drawer.drawCanvas()

    def check_resize(self, instance, x, y):
        self.drawer.drawCanvas()
