from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class MyApp(App):
    def build(self):
        bl = BoxLayout(
            orientation='horizontal',
            padding=[50],
            spacing=10)
        bl.add_widget(
            Button(text="0",
                   font_size=16,
                   on_press=self.btn_press,
                   background_color=[1, 0, 0, 1],
                   background_normal=''
                   )
        )

        bl.add_widget(
            Button(text="0",
                   font_size=16,
                   on_press=self.btn_press,
                   background_color=[1, 0, 0, 1],
                   background_normal=''
                   ))

        return bl

    def btn_press(self, instance):
        instance.text = str(eval(instance.text) + 1)


if __name__ == '__main__':
    MyApp().run()
