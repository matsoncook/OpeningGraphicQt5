import sys
from PyQt5.QtWidgets import QApplication, QOpenGLWidget
from PyQt5.QtCore import Qt, QTimer, QElapsedTimer
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
import numpy as np

from base.base_object import GroupObject
from glowing_circle.glowing_circle_gl import GlowingCircle
from shaders import Shaders


class GlowingCircleWidget(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.world = GroupObject("World")
        self.glowing_circle1 = GlowingCircle(name="GlowingCircle1",y=0.25)
        self.glowing_circle2 = GlowingCircle(name="GlowingCircle2",y=-0.25)

        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.start(16)

        self.timer = QElapsedTimer()
        self.timer.start()


    def initializeGL(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        shaders = Shaders()
        self.glowing_circle1.init_shaders(shaders)
        self.glowing_circle1.init_geometry()

        self.glowing_circle2.init_shaders(shaders)
        self.glowing_circle2.init_geometry()





    def paintGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        glDisable(GL_DEPTH_TEST)

        self.glowing_circle1.paintGL(self)
        self.glowing_circle2.paintGL(self)

    def update_animation(self):
        # Update the circle's position (e.g., move in a sine wave)
        t = QTimer().remainingTime() / 1000.0  # Time in seconds

        self.glowing_circle1.update(self.timer.elapsed())
        self.glowing_circle2.update(self.timer.elapsed())


        self.update()  # Trigger a redraw

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)

        self.glowing_circle1.resizeGL(w, h)
        self.glowing_circle2.resizeGL(w, h)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GlowingCircleWidget()
    window.resize(800, 800)
    window.show()
    sys.exit(app.exec_())
