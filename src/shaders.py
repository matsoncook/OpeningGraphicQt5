from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram

from glowing_circle.glowing_circle_shader import GlowingCircleShader
from glowing_rectangle.glowing_rectangle_shader1 import GlowingRectangleShader
from line.line_shader import LineShader


class Shaders:
    def __init__(self):
        gc = GlowingCircleShader()

        self.glowing_circle_shader_program = compileProgram(
            compileShader(gc.glowing_circle_vertex_shader, GL_VERTEX_SHADER),
            compileShader(gc.glowing_circle_fragment_shader, GL_FRAGMENT_SHADER)
        )

        gr = GlowingRectangleShader()

        self.glowing_rectangle_shader_program = compileProgram(
            compileShader(gr.glowing_rectangle_vertex_shader, GL_VERTEX_SHADER),
            compileShader(gr.glowing_rectangle_fragment_shader, GL_FRAGMENT_SHADER)
        )

        self.line_shader = LineShader()

