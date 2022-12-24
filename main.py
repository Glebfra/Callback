from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivymd.uix.boxlayout import MDBoxLayout
from numpy import *
from kivymd.uix.tab import MDTabsBase, MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout

class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''
    content_text = ''


class Container(MDBoxLayout):
    pass


class MyApp(MDApp):
    theme_cls = ThemeManager()

    def build(self):
        Builder.load_file('fig.kv')
        self.theme_cls.theme_style = 'Amber'
        self.theme_cls.material_style = "Amber"
        self.theme_cls.primary_palette = "Amber"
        self.theme_cls.accent_palette = "Red"
        return Container()

    def btn_press(self, instance):
        instance.text = str(eval(instance.text) + 1)


if __name__ == '__main__':
    MyApp().run()
