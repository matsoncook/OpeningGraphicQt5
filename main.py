import sys
from PyQt5.QtWidgets import QApplication, QOpenGLWidget
from PyQt5.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
import numpy as np


class GlowingCircleWidget(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.shader_program = None
        self.vao = None

    def initializeGL(self):
        self.init_shaders()
        self.init_geometry()

    def init_shaders(self):
        vertex_shader = """
        #version 330 core
        layout(location = 0) in vec2 position;
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
            float intensity = smoothstep(circle_radius, circle_radius * 0.9, dist);
            vec3 color = mix(vec3(1.0, 0.8, 0.4), vec3(0.0), intensity);
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

    def paintGL(self):
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(self.shader_program)

        # Set uniform values
        resolution = self.size()
        glUniform2f(glGetUniformLocation(self.shader_program, "resolution"), resolution.width(), resolution.height())
        glUniform2f(glGetUniformLocation(self.shader_program, "circle_center"), 0.0, 0.0)
        glUniform1f(glGetUniformLocation(self.shader_program, "circle_radius"), 0.3)

        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GlowingCircleWidget()
    window.resize(800, 800)
    window.show()
    sys.exit(app.exec_())
