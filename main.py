from kivy.app import App
from kivy.uix.label import Label

from fragmentcompute import FragmentCompute

class MainApp(App):
    def build(self):
        fg = FragmentCompute(2)

        fg.compute()

        lines = [
            fg.texture().size,
            repr(fg.data())
        ]
        text = '\n'.join((str(line) for line in lines))
        return Label(text=text)

if __name__ == '__main__':
    MainApp().run()
