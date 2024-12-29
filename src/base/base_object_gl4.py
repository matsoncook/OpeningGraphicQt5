from typing import List

from base.animator import Animator
from base.base_object import BaseObject
from shaders import Shaders

from OpenGL.GL import *


class BaseObjectGL4(BaseObject):
    def __init__(self, name):
        super().__init__(name)
        self.shader_program = None



    def paint_prepare(self):
        glUseProgram(self.shader_program)
        model_loc = glGetUniformLocation(self.shader_program, 'model')
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, self.world_matrix)

    # def paint_gl(self, context):
    #     glBindVertexArray(self.vao)
    #     glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)


class GroupObject(BaseObject):
    def __init__(self, name):
        super().__init__(name)


