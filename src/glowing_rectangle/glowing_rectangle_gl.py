import numpy as np

from base.base_object_gl4 import BaseObjectGL4
from OpenGL.GL import *

from shaders import Shaders


class GlowingRectangle(BaseObjectGL4):
    def __init__(self,name, xyxy:(float,float,float,float) = (-0.5, 0.5, 0.5, -0.5)):
        super().__init__(name)
        self.xyxy = xyxy

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
        position_loc = glGetAttribLocation(self.shader_program, 'position')
        glVertexAttribPointer(position_loc, 3, GL_FLOAT, GL_FALSE, 3 * vertices.itemsize, None)
        glEnableVertexAttribArray(position_loc)

        glBindVertexArray(0)


        self.vertex_array_object = self.vao

    def paint_gl(self,context):

        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)