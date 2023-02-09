from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty

import json

from kivy.uix.popup import Popup
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.menu import MDDropdownMenu

from kivy.metrics import dp

from FrontEnd.Drawer import Drawer
import os


class Container(MDBoxLayout):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        menu_items = [
            {
                "id": 'neyman',
                "viewclass": "IconListItem",
                "text": "fon Neyman's background",
                "height": dp(56),
            },
            {
                "viewclass": "IconListItem",
                "text": "Moore's background",
                "height": dp(56),
            }
        ]

        super().__init__(*args, **kwargs)
        self.menu = MDDropdownMenu(
            elevation=1,
            radius=0,
            caller=self.ids.drop_item,
            items=menu_items,
            position="center",
            width_mult=4,
        )
        self.menu.bind()

    def set_item(self, text_item):
        self.ids.drop_item.set_item(text_item)
        self.menu.dismiss()

    def menu_callback(self, text_item):
        print(text_item)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        print('Callback')
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        self.ids.FilePath.text = str(filename)[2:-2]
        self.dismiss_popup()

    def save(self, path, filename):
        with open(f'{path}.json', 'w') as stream:
            json.dump(self.calculations, stream)
        self.dismiss_popup()


class LoadDialog(MDFloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(MDFloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


class IconListItem(OneLineIconListItem):
    icon = StringProperty()
