
from OpenGL.GL import *

import numpy as np

from base.base_object import BaseObject
from glowing_circle.glowing_circle_animator import MoveRight_1
from shaders import Shaders


class GlowingCircle(BaseObject):
    def __init__(self, y =0.0):
        super().__init__()

        self.shader_program = None
        self.vao = None


        self.circle_center = [0.0, y]
        self.circle_radius = 0.2

        self.a = MoveRight_1(self)
        self.add_animator(self.a)

        self.circle_color = [1.0, 0.0, 0.0]


    def init_shaders(self,shader: Shaders):

        self.shader_program = shader.glowing_circle_shader_program

    def init_geometry(self):
        vertices = np.array([
            -1.0, -1.0,
            1.0, -1.0,
            -1.0, 1.0,
            1.0, 1.0,
        ], dtype=np.float32)

        self.vao = glGenVertexArrays(1)
        vbo = glGenBuffers(1)

        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)

    def paintGL(self,context):


        glUseProgram(self.shader_program)

        # Set uniform values
        resolution = context.size()
        glUniform2f(glGetUniformLocation(self.shader_program, "resolution"), resolution.width(),
                    resolution.height())
        glUniform2f(glGetUniformLocation(self.shader_program, "circle_center"), *self.circle_center)
        glUniform1f(glGetUniformLocation(self.shader_program, "circle_radius"), self.circle_radius)
        glUniform3f(glGetUniformLocation(self.shader_program, "circle_color"), *self.circle_color)

        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

    def resizeGL(self, w, h):
        pass

    def update(self,time_ms):
        super().update(time_ms)

