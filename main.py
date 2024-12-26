import sys
from PyQt5.QtWidgets import QApplication, QOpenGLWidget
from PyQt5.QtCore import Qt, QTimer, QElapsedTimer
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
import numpy as np

from glowing_circle import GlowingCircle


class GlowingCircleWidget(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.glowing_circle = GlowingCircle()

        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.start(16)

        self.timer = QElapsedTimer()
        self.timer.start()


    def initializeGL(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.glowing_circle.init_shaders()
        self.glowing_circle.init_geometry()





    def paintGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        glDisable(GL_DEPTH_TEST)

        self.glowing_circle.paintGL(self)

    def update_animation(self):
        # Update the circle's position (e.g., move in a sine wave)
        t = QTimer().remainingTime() / 1000.0  # Time in seconds

        self.glowing_circle.update(self.timer.elapsed())


        self.update()  # Trigger a redraw

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)

        self.glowing_circle.resizeGL(w, h)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GlowingCircleWidget()
    window.resize(800, 800)
    window.show()
    sys.exit(app.exec_())
