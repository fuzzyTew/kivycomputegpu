from kivy.app import App
from kivy.logger import Logger, LOG_LEVELS, LoggerHistory
from kivy.uix.label import Label

from kivy.graphics.texture import Texture

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
                gl_FragColor = vec4(idxs.x, ratios.x, lastcol.b + 0.125, 0.0);
            }
        """, 4)

        other = Texture.create(size = (4,1))
        #+ther.blit

        fg.set_extra_textures([
        ])

        data1 = fg.compute().download()
        data2 = fg.compute().download()

        lines = [
            fg.texture().size,
            [n for n in data1],
            [n for n in data2],
        ]
        for item in LoggerHistory.history:
            lines.append(item.getMessage())
        
        text = '\n'.join((str(line) for line in lines))
        return WrappingLabel(text=text)

if __name__ == '__main__':
    MainApp().run()
