from kivy.app import App
from kivy.logger import Logger, LOG_LEVELS, LoggerHistory
from kivy.uix.label import Label

from fragmentcompute import FragmentCompute

class WrappingLabel(Label):
    def on_size(self, instance, size):
        self.text_size = size

class MainApp(App):
    def build(self):
        Logger.setLevel(LOG_LEVELS["info"])

        fg = FragmentCompute(3)

        fg.compute()

        data = fg.download()

        lines = [
            fg.texture().size,
            [n for n in data],
        ]
        for item in LoggerHistory.history:
            lines.append(item.getMessage())
        
        text = '\n'.join((str(line) for line in lines))
        return WrappingLabel(text=text)

if __name__ == '__main__':
    MainApp().run()
