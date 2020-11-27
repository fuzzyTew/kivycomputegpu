# let's make a kivy tool
# for computing with fragments.
# we can do something like making
# 1-dimensional fbos and rendering to them.

# fbo is a rendercontext. so we can likely
# pass a shader to it

from kivy.graphics import Callback, Color, Fbo, Rectangle
import kivy.graphics.opengl as gl
from kivy.graphics.texture import Texture
from kivy.graphics.transformation import Matrix
from kivy.logger import Logger

class FragmentCompute:
    def __init__(self, length1, length2 = 1):
        size = (length1, length2)

        # it doesn't look like we can use float textures on mobile kivy, but people sometimes interconvert floats with 32bit rgba in shaders.
        # we would then have 3 shaders or texture rows or such, for x coord, y coord, angle, etc

        #Logger.info('float: ' + str(gl.getExtension('OES_texture_float')))
        texture = Texture.create(
            size = size,
            #bufferfmt = 'float'
        )
        self._fbo = Fbo(
            size = size,
            texture = texture,
            vs = """
            #ifdef GL_ES
                precision highp float;
            #endif
            
            /* Outputs to the fragment shader */
            varying vec2 tex_coord0;
            
            /* vertex attributes */
            attribute vec2     vPosition;
            attribute vec2     vTexCoords0;
            
            /* uniform variables */
            uniform mat4       projection_mat;
            void main (void) {
                tex_coord0 = vTexCoords0;
                gl_Position = projection_mat * vec4(vPosition.xy, 0.0, 1.0);
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

            /* uniform variables */
            uniform mat4 frag_coord2idx;
            uniform mat4 frag_coord2ratio;

            void main (void){
                vec2 idxs = (frag_coord2idx * gl_FragCoord).xy;
                vec2 ratios = (frag_coord2ratio * gl_FragCoord).xy;
                vec4 lastcol = texture2D(texture0, ratios);
                gl_FragColor = vec4(idxs.x, ratios.x, lastcol.b + 0.125, 0.0);
            }
            """)

        # these matrices are to transform
        # window coordinates into data
        # coordinates
        centermat = Matrix()
        centermat.translate(-.5,-.5,-.5)
        idxscale = 1.0 / 255.0;
        idxmat = Matrix()
        idxmat.scale(idxscale, idxscale, idxscale)
        self._fbo['frag_coord2idx'] = idxmat.multiply(centermat)
        ratiomat = Matrix()
        ratiomat.scale(1.0 / length1, 1.0 / length2, 1.0)
        self._fbo['frag_coord2ratio'] = ratiomat

        self._fbo.add_reload_observer(self._populate_fbo)
        self._populate_fbo(self._fbo)
    def texture(self):
        return self._fbo.texture
    def download(self):
        ## cgl requires cython,
        ## but glReadPixels is used in
        ## fbo.py, and could be used to
        ## get RGB instead of RGBA, since
        ## A is presently drawn blended,
        ## and maybe save a memory copy.
        #width, height = self._fbo.size
        #data = array('B', [1] * width * height * 4)
        #self._fbo.bind()
        #cgl.cgl.glPixelStorei(GL_PACK_ALIGNMENT, 1)
        #cgl.cgl.glReadPixels(0, 0, width, height, cgl.GL_RGB, cgl.GL_UNSIGNED_BYTE, data)
        #self._fbo.release()
        #return data
        return bytearray(self._fbo.pixels)
    def compute(self):
        self._rectangle.texture = self._fbo.texture
        self._fbo.draw()
        return self
    def __setitem__(self, name, value):
        self._fbo[name] = value
        # if isinstance(value, Texture):

    def _populate_fbo(self, fbo):
        with fbo:
            Callback(self._set_blend_mode)
            self._rectangle = Rectangle(size = self._fbo.size)
            Callback(self._unset_blend_mode)
    # opaque blend mode provides for use of the alpha channel for data
    def _set_blend_mode(self, instruction = None):
        gl.glBlendFunc(gl.GL_ONE, gl.GL_ZERO);
        gl.glBlendFuncSeparate(gl.GL_ONE, gl.GL_ZERO, gl.GL_ONE, gl.GL_ZERO);
    def _unset_blend_mode(self, instruction = None):
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA);
        gl.glBlendFuncSeparate(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA, gl.GL_ONE, gl.GL_ONE);
            
