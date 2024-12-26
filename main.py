import sys
from PyQt5.QtWidgets import QApplication, QOpenGLWidget
from PyQt5.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
import numpy as np

from glowing_circle import GlowingCircle


class GlowingCircleWidget(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.glowing_circle = GlowingCircle()


    def initializeGL(self):
        self.glowing_circle.init_shaders()
        self.glowing_circle.init_geometry()





    def paintGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        self.glowing_circle.paintGL(self)



    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)

        self.glowing_circle.resizeGL(w, h)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GlowingCircleWidget()
    window.resize(800, 800)
    window.show()
    sys.exit(app.exec_())
