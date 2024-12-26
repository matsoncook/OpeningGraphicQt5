
from OpenGL.GL import *

import numpy as np

from base.base_object import BaseObject
from glowing_circle.glowing_circle_animator import MoveRight_1
from shaders import Shaders

from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram


class GlowingLine(BaseObject):
    def __init__(self, y =0.0):
        super().__init__()

        self.program = None
        self.vao = None
        self.vbo = None


        self.rect_pos = np.array([-0.2, -0.2, 0.2, -0.2, 0.2, 0.2, -0.2, 0.2], dtype=np.float32)
        self.rect_speed = [0.01, 0.01]
        self.rect_scale = [1.0, 1.0]
        self.scale_dir = [0.01, 0.01]


    def init_shaders(self,shader: Shaders):
        # Vertex and Fragment Shader source
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

    def init_geometry(self):
        # Create VAO and VBO
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)

        glBindVertexArray(self.vao)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.rect_pos.nbytes, self.rect_pos, GL_DYNAMIC_DRAW)

        position = glGetAttribLocation(self.program, "position")
        glVertexAttribPointer(position, 2, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(position)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def paintGL(self,context):

        glUseProgram(self.program)

        # Create transformation matrix
        transform = np.eye(4, dtype=np.float32)
        transform[0, 0] = self.rect_scale[0]
        transform[1, 1] = self.rect_scale[1]
        transform[3, 0] = self.rect_speed[0]
        transform[3, 1] = self.rect_speed[1]

        transform_location = glGetUniformLocation(self.program, "transform")
        glUniformMatrix4fv(transform_location, 1, GL_TRUE, transform)

        glBindVertexArray(self.vao)
        glDrawArrays(GL_QUADS, 0, 4)
        glBindVertexArray(0)

    def resizeGL(self, w, h):
        pass

    def update(self,time_ms):
        super().update(time_ms)

