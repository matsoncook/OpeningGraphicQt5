from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram

class LineShader:
    def __init__(self):
        VERTEX_SHADER = """
                #version 330
                in vec2 position;
                uniform mat4 transform;
                void main() {
                    gl_Position = transform * vec4(position, 0.0, 1.0);
                }
                """

        FRAGMENT_SHADER = """
                #version 330
                out vec4 FragColor;
                void main() {
                    FragColor = vec4(1.0, 0.5, 0.2, 1.0);
                }
                """
        self.program = compileProgram(
            compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
            compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER),
        )