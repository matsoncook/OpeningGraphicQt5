
from OpenGL.GL import *

import numpy as np

from base.base_object import BaseObject
from base.base_object_gl4 import BaseObjectGL4

from shaders import Shaders


class GlowingCircle(BaseObjectGL4):
    def __init__(self, name,  y =0.0):
        super().__init__(name)


        self.vao = None


        self.circle_center = [0.0, y]
        self.world_matrix[3, 1] = y
        self.circle_radius = 0.05



        self.circle_color = [1.0, 0.0, 0.0]

    def set_circle_center_x(self,x):
        self.circle_center[0] = x
        self.world_matrix[3, 0] = x

    def init_gl(self,shaders: Shaders):
        self.init_shaders(shaders)
        self.init_geometry()
    def init_shaders(self,shader: Shaders):

        self.shader_program = shader.glowing_circle_shader_program

    def init_geometry(self):
        vertices = np.array([
            -1.0, -1.0, 0.0,
            1.0, -1.0, 0.0,
            -1.0, 1.0, 0.0,
            1.0, 1.0, 0.0
        ], dtype=np.float32)

        vertices = vertices *0.15

        self.vao = glGenVertexArrays(1)
        vbo = glGenBuffers(1)

        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

    def paint_gl(self,context):

        glUseProgram(self.shader_program)

        # Set uniform values
        screen_resolution = context.size()
        glUniform2f(glGetUniformLocation(self.shader_program, "resolution"), screen_resolution.width(),
                    screen_resolution.height())
        glUniform2f(glGetUniformLocation(self.shader_program, "circle_center"), *self.circle_center)
        glUniform1f(glGetUniformLocation(self.shader_program, "circle_radius"), self.circle_radius)
        glUniform3f(glGetUniformLocation(self.shader_program, "circle_color"),  *self.circle_color)

        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

    def resize_gl(self, w, h):
        pass

    # def update(self,time_ms):
    #     super().update(time_ms)

