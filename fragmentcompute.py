# let's make a kivy tool
# for computing with fragments.
# we can do something like making
# 1-dimensional fbos and rendering to them.

# fbo is a rendercontext. so we can likely
# pass a shader to it

from kivy.graphics import Fbo, Rectangle

class FragmentCompute:
    def __init__(self, length1, length2 = 1):
        self._fbo = Fbo(
            size = (length1, length2),
            fs = """
            $HEADER$
            void main (void){
                //gl_FragColor = frag_color * texture2D(texture0, tex_coord0);
                gl_FragColor = tex_coord0
            }
            """)
    def texture(self):
        return self._fbo.texture
    def data(self):
        return self._fbo.pixels
    def compute(self):
        self._fbo.draw()
        return self
