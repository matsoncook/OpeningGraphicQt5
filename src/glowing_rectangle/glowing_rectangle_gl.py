import numpy as np

from base.base_object_gl4 import BaseObjectGL4
from OpenGL.GL import *

from shaders import Shaders


class GlowingRectangle(BaseObjectGL4):
    def __init__(self,name, xyxy:(float,float,float,float) = (-0.5, 0.5, 0.5, -0.5)):
        super().__init__(name)
        self.xyxy = xyxy

    def set_circle_center_x(self, x):

        self.world_matrix[3, 0] = x
    def init_gl(self,shaders: Shaders):
        self.shader_program = shaders.glowing_rectangle_shader_program

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        x1,y1,x2,y2 = self.xyxy

        vertices = np.array([
            x1, y2, 0.0,
            x2, y2, 0.0,
            x2, y1, 0.0,
            x1, y1, 0.0
        ], dtype=np.float32)

        indices = np.array([
            0, 1, 2,
            2, 3, 0
        ], dtype=np.uint32)

        # Vertex Buffer Object
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        # Element Buffer Object
        ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

        # Vertex attribute pointers
        position_loc = glGetAttribLocation(self.shader_program, 'aPosition')
        glVertexAttribPointer(position_loc, 3, GL_FLOAT, GL_FALSE, 3 * vertices.itemsize, None)
        glEnableVertexAttribArray(position_loc)

        glBindVertexArray(0)


        self.vertex_array_object = self.vao

    def paint_gl(self,context):
        uColor_loc = glGetUniformLocation(self.shader_program, "uColor")
        uGlowWidth_loc = glGetUniformLocation(self.shader_program, "uGlowWidth")
        uGlowSoft_loc = glGetUniformLocation(self.shader_program, "uGlowSoft")
        # Set some uniform values for color and glow
        glUniform3f(uColor_loc, 1.0, 1.0, 1.0)  # Orange-ish
        glUniform1f(uGlowWidth_loc, 0.05)  # Glow extends 0.05 in y-direction
        glUniform1f(uGlowSoft_loc, 20.0)  # Larger = sharper fade, smaller = slower fade

        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)