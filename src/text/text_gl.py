import freetype

from base.base_object import BaseObject
from shaders import Shaders

from OpenGL.GL import *

class TextGl(BaseObject):
    def __init__(self,name):
        super().__init__(name)
        self.vbo = None
        self.vertices = []
        self.face = freetype.Face(r"C:\Windows\Fonts\Arial.ttf")  # Replace with your font path
        self.face.set_char_size(48 * 64)

    def init_gl(self,shaders:Shaders):
        # self.prepare_text_geometry("Hello, OpenGL!")
        self.prepare_text_geometry("e")

    def prepare_text_geometry(self, text):
        """
        Generate vertex data for the given text and load it into a VBO.
        """
        pen_x, pen_y = 0, 0  # Cursor position
        self.vertices = []

        for char in text:
            self.face.load_char(char)
            glyph = self.face.glyph
            outline = glyph.outline

            start_idx = len(self.vertices) // 2
            for point in outline.points:
                self.vertices.extend([
                    (point[0] / 64.0 + pen_x) / 100.0 -0.5,  # Normalize to [-1, 1]
                    (point[1] / 64.0 + pen_y) / 100.0 -0.0,
                ])

            for contour_start, contour_end in zip([0] + outline.contours[:-1], outline.contours):
                for i in range(contour_start, contour_end):
                    self.vertices.extend(self.vertices[start_idx + i * 2:start_idx + (i + 1) * 2])

            pen_x += glyph.advance.x / 64.0  # Move cursor for the next character

        # Convert to OpenGL buffer
        self.vertices = (GLfloat * len(self.vertices))(*self.vertices)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices, GL_STATIC_DRAW)

    def paint_gl(self,context):

        glColor3f(1.0, 1.0, 1.0)

        if self.vbo:
            glEnableClientState(GL_VERTEX_ARRAY)
            glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
            glVertexPointer(2, GL_FLOAT, 0, None)
            glDrawArrays(GL_LINE_STRIP, 0, len(self.vertices) // 2)
            glDisableClientState(GL_VERTEX_ARRAY)

    def resize_gl(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-1.0, 1.0, -1.0, 1.0, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)