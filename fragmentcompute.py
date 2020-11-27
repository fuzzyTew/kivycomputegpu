# let's make a kivy tool
# for computing with fragments.
# we can do something like making
# 1-dimensional fbos and rendering to them.

# fbo is a rendercontext. so we can likely
# pass a shader to it

from kivy.graphics import Color, Fbo, Rectangle
#from kivy.graphics.opengl import glReadPixels
from kivy.graphics.transformation import Matrix
from kivy.logger import Logger

class FragmentCompute:
    def __init__(self, length1, length2 = 1):
        self._fbo = Fbo(
            size = (length1, length2),
            vs = """
            $HEADER$
            void main (void) {
                frag_color = color * vec4(1.0, 1.0, 1.0, opacity);
                tex_coord0 = vTexCoords0;
                gl_Position = projection_mat * modelview_mat * vec4(vPosition.xy, 0.0, 1.0);
            }
            """,
            fs = """
            #ifdef GL_ES
                precision highp float;
            #endif

            /* Outputs from the vertex shader */
            varying vec4 frag_color;
            varying vec2 tex_coord0;

            /* uniform texture samplers */
            uniform sampler2D texture0;

            uniform mat4 frag_modelview_mat;
            uniform mat4 frag_coord2idx;
            uniform mat4 frag_coord2ratio;

            void main (void){
                //gl_FragColor = frag_color * texture2D(texture0, tex_coord0);
                vec4 coord = gl_FragCoord.xyzw;
                vec2 idxs = (frag_coord2idx * coord).xy;
                vec2 ratios = (frag_coord2ratio * coord).xy;
                coord = vec4(idxs.x, ratios.x, 0.0, 1.0);//frag_coord2idx * coord;//vec4(idxs.xy, 0.0, 0.0);
                gl_FragColor = coord;//vec4(coord.xyzw);
                //gl_FragColor = vec4(gl_FragCoord.x - 0.5,1.0,1.0,1.0);
            }
            """)
        centermat = Matrix()
        centermat.translate(-.5,-.5,-.5)
        idxscale = 1.0 / 255.0;
        idxmat = Matrix()
        idxmat.scale(idxscale, idxscale, idxscale)
        self._fbo['frag_coord2idx'] = idxmat.multiply(centermat)
        ratiomat = Matrix()
        ratiomat.scale(1.0 / length1, 1.0 / length2, 1.0)
        self._fbo['frag_coord2ratio'] = ratiomat#.multiply(centermat)
        with self._fbo:
            Color(1,1,1,1)
            Rectangle(size = self._fbo.size)
    def texture(self):
        return self._fbo.texture
    def download(self):
        #width, height = self._fbo.size
        #data = array('B', [1] * width * height * 4)
        #self._fbo.bind()
        #cgl.cgl.glPixelStorei(GL_PACK_ALIGNMENT, 1)
        #cgl.cgl.glReadPixels(0, 0, width, height, cgl.GL_RGB, cgl.GL_UNSIGNED_BYTE, data)
        #self._fbo.release()
        #return data
        return bytearray(self._fbo.pixels)
    def compute(self):
        self._fbo.draw()
        return self
