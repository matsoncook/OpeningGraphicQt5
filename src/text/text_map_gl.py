import freetype

from base.base_object import BaseObject
from shaders import Shaders

from OpenGL.GL import *

from PIL import Image, ImageDraw, ImageFont
import numpy as np

class TextMapGl(BaseObject):
    def __init__(self,name,text, font_path=r"C:\Windows\Fonts\arial.ttf", font_size=32):
        super().__init__(name)

        self.text = text
        self.font_path = font_path
        self.font_size = font_size
        self.texture_id = None
        self.width = 0
        self.height = 0


        # self.vbo = None
        # self.vertices = []
        # self.face = freetype.Face(r"C:\Windows\Fonts\Arial.ttf")  # Replace with your font path
        # self.face.set_char_size(48 * 64)

    def init_gl(self,shaders:Shaders):
        # self.prepare_text_geometry("Hello, OpenGL!")
        # self.create_text_image()
        # self.load_texture
        self.load_texture()

    def load_texture(self):
        """
        Load the text as an OpenGL texture.
        """
        image = self.create_text_image()
        image_data = np.array(image, dtype=np.uint8)

        # Generate a texture ID
        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)

        # Set texture parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # Upload the texture to the GPU
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0,
                     GL_RGBA, GL_UNSIGNED_BYTE, image_data)

    def create_text_image(self):
        """
        Create an image with Pillow containing the text.
        """
        font = ImageFont.truetype(self.font_path, self.font_size)
        text_bbox = font.getbbox(self.text)
        text_size = (text_bbox[2] - text_bbox[0], text_bbox[3] )
        self.width, self.height = text_size


        # Create an RGBA image
        image = Image.new("RGBA", text_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), self.text, font=font, fill=(255, 255, 255, 255))
        return image


    def paint_gl(self,context):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-1, 1, -1, 1, -1, 1)  # Orthographic projection
        glMatrixMode(GL_MODELVIEW)

        glLoadIdentity()
        glPushMatrix()
        # glRotate(180,1,0,0)
        glTranslate(self.translate[0],self.translate[1],self.translate[2])
        glRotate(180, 1, 0, 0)
        glColor3f(1.0, 1.0, 1.0)


        self.aspect = self.width / self.height
        len = 1.0
        height = len / self.aspect
        x = - len/2
        y = height /2

        x_to = x + len
        y_to = y - height
        if not self.texture_id:
            return
        # Enable texturing
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)




        # Draw a textured quad
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0)
        glVertex2f(x, y)

        glTexCoord2f(1.0, 1.0)
        glVertex2f(x_to, y)

        glTexCoord2f(1.0, 0.0)
        glVertex2f(x_to, y_to)

        glTexCoord2f(0.0, 0.0)
        glVertex2f(x, y_to)
        glEnd()

        glDisable(GL_TEXTURE_2D)

        glPopMatrix()


    def resize_gl(self, width, height):
        #glViewport(0, 0, width, height)
        # glMatrixMode(GL_PROJECTION)
        # glLoadIdentity()
        # glOrtho(-1.0, 1.0, -1.0, 1.0, -1.0, 1.0)
        # glMatrixMode(GL_MODELVIEW)
        pass