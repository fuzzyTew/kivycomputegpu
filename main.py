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

        fg = FragmentCompute("""
            uniform sampler2D other_tex;

            void main (void){
                vec2 idxs = (frag_coord2idx * gl_FragCoord).xy;
                vec2 ratios = (frag_coord2ratio * gl_FragCoord).xy;
                vec4 lastcol = texture2D(last_tex, ratios);
                gl_FragColor = vec4(idxs.x, ratios.x, lastcol.b + 0.125, texture2D(other_tex, ratios).a);
            }
        """, 4)

        fg.set_extra_textures([
            [4, 4, 4, 4,
             3, 3, 3, 3,
             2, 2, 2, 2,
             1, 1, 1, 1]
        ])
        fg['other_tex'] = 1



        data1 = fg.compute().download()
        data2 = fg.compute().download()

        data3 = fg.extra_textures[0].pixels

        lines = [
            fg.texture().size,
            [n for n in data1],
            [n for n in data2],
            [n for n in data3],
        ]
        for item in LoggerHistory.history:
            lines.append(item.getMessage())
        
        text = '\n'.join((str(line) for line in lines))
        return WrappingLabel(text=text)

if __name__ == '__main__':
    MainApp().run()
