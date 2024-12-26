import sys
from PyQt5.QtWidgets import QApplication, QOpenGLWidget
from PyQt5.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
import numpy as np

from base.base_object import BaseObject
from glowing_circle_animations.glowing_circle_animator import MoveRight_1


class GlowingCircle(BaseObject):
    def __init__(self):
        super().__init__()

        self.shader_program = None
        self.vao = None


        self.circle_center = [0.0, 0.0]
        self.circle_radius = 0.2
        self.direction = 1
        self.previous_time_ms = 0
        #self.circle_position = [1.0, 0.0]

        # def initializeGL(self):
    #     self.init_shaders()
    #     self.init_geometry()
        self.velocity = 1 #Half a screen per sec
        self.a = MoveRight_1(self)
        self.add_animator(self.a)


    def init_shaders(self):
        vertex_shader = """
           #version 330 core
           layout(location = 0) in vec2 position;
           //uniform vec2 circle_position;
           void main() {
               gl_Position = vec4(position, 0.0, 1.0);
           }
           """
        fragment_shader = """
           #version 330 core
           out vec4 fragColor;
           uniform vec2 resolution;
           uniform vec2 circle_center;
           uniform float circle_radius;

           void main() {
               vec2 uv = gl_FragCoord.xy / resolution;
               vec2 p = uv * 2.0 - 1.0;
               float dist = length(p - circle_center);
               //float intensity = smoothstep(circle_radius, circle_radius * 0.9, dist);
               float intensity = smoothstep(circle_radius*1.5, circle_radius * 0.8, dist);//increase glow
               //vec3 color = mix(vec3(1.0, 0.8, 0.4), vec3(0.0), intensity);
               vec3 color = mix(vec3(1.0, 1.0, 1.0), vec3(1.0), intensity); //white
               fragColor = vec4(color, 1.0 - intensity);
           }
           """
        self.shader_program = compileProgram(
            compileShader(vertex_shader, GL_VERTEX_SHADER),
            compileShader(fragment_shader, GL_FRAGMENT_SHADER)
        )

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
        #glUniform2f(glGetUniformLocation(self.shader_program, "circle_position"), *self.circle_position)

        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

    def resizeGL(self, w, h):
        pass

    def update(self,time_ms):
        super().update(time_ms)
        # p = self.previous_time_ms
        # t = (time_ms - self.previous_time_ms) /1000
        # self.previous_time_ms = time_ms
        # if p == 0:
        #     return
        #
        # velocity = self.velocity * t
        #
        # c_x = self.circle_center[0]
        # c_x += velocity * self.direction
        #
        # if c_x >= 1.0 or c_x <= -1.0:
        #    self.direction *= -1
        #
        # c_x += (0.01 * self.direction)
        # self.circle_center[0] = c_x
