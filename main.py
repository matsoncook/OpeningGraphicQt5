import sys
from PyQt5.QtWidgets import QApplication, QOpenGLWidget
from PyQt5.QtCore import Qt, QTimer, QElapsedTimer
from OpenGL.GL import *

from base.base_object import GroupObject
from glowing_circle.glowing_circle_animator import MoveRight_1
from glowing_circle.glowing_circle_gl import GlowingCircle
from glowing_rectangle.glowing_rectangle_gl import GlowingRectangle
from line.line_gl import GlowingLine
from shaders import Shaders
from text.text_gl import TextGl
from text.text_map_gl import TextMapGl
from texture.texture_gl import TextureGl


class GlowingCircleWidget(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.world = GroupObject("World")
        self.setup_world()
       # shaders = Shaders()




        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.start(16)

        self.timer = QElapsedTimer()
        self.timer.start()

    def setup_world(self):






        # self.line1 = GlowingLine(name = "line1",y=0.25)
        # self.world.add_child(self.line1)
        #
        # self.line2 = GlowingLine(name="line2",y=-0.25)
        # self.world.add_child(self.line2)



        self.glowing_rectangle1 = GlowingRectangle(name="glowing_rectangle1",xyxy=(-2, 0.05, 0, -0.05))
        self.glowing_rectangle1.world_matrix[3,1] = 0.05
        self.world.add_child(self.glowing_rectangle1)
        self.glowing_rectangle1.add_animator(MoveRight_1(self.glowing_rectangle1 ))

        self.glowing_rectangle2 = GlowingRectangle(name="glowing_rectangle2", xyxy=(-2, 0.05, 0, -0.05))
        self.glowing_rectangle2.world_matrix[3, 1] = -0.05
        self.world.add_child(self.glowing_rectangle2)
        self.glowing_rectangle2.add_animator(MoveRight_1(self.glowing_rectangle2))

        self.glowing_circle1 = GlowingCircle(name="GlowingCircle1", y=0.05)
        self.world.add_child(self.glowing_circle1)
        self.glowing_circle1.add_animator(MoveRight_1(self.glowing_circle1 ))

        self.glowing_circle2 = GlowingCircle(name="GlowingCircle2", y=-0.05)
        self.world.add_child(self.glowing_circle2)
        self.glowing_circle2.add_animator(MoveRight_1(self.glowing_circle2 ))

        # self.text_future = TextMapGl("Text_future", "FUTURE")
        # self.text_future.translate = (0,.15,0)
        # self.world.add_child(self.text_future)
        #
        # self.text_runway = TextMapGl("Text_runway", "RUNWAY")
        # self.text_runway.translate = (0,-.15,0)
        # self.world.add_child(self.text_runway)

        # self.text_future = TextureGl("Text_future","MicrosoftTeams-image01.png")
        # #self.text_future.translate = (0, .15, 0)
        # self.world.add_child(self.text_future)



    def initializeGL(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDepthMask(GL_TRUE);

        shaders = Shaders()

        self.world.init(shaders)

        # self.glowing_circle1.init_shaders(shaders)
        # self.glowing_circle1.init_geometry()
        #
        # self.glowing_circle2.init_shaders(shaders)
        # self.glowing_circle2.init_geometry()





    def paintGL(self):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        # glClearColor(0.0, 0.0, 0.0, 1.0)
        # glClear(GL_COLOR_BUFFER_BIT)
        # glDisable(GL_DEPTH_TEST)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.world.paint(self)

        # self.glowing_circle1.paintGL(self)
        # self.glowing_circle2.paintGL(self)

    def update_animation(self):
        # Update the circle's position (e.g., move in a sine wave)
        t = QTimer().remainingTime() / 1000.0  # Time in seconds

        # self.glowing_circle1.update(self.timer.elapsed())
        # self.glowing_circle2.update(self.timer.elapsed())
        self.world.update(self.timer.elapsed())

        self.update()  # Trigger a redraw

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)

        # self.glowing_circle1.resizeGL(w, h)
        # self.glowing_circle2.resizeGL(w, h)

        self.world.resize(w, h)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GlowingCircleWidget()
    window.resize(800, 800)
    window.show()
    sys.exit(app.exec_())
