import freetype

from base.base_object import BaseObject
from shaders import Shaders

from OpenGL.GL import *

from PIL import Image, ImageDraw, ImageFont
import numpy as np

from texture.texture_gl import TextureGl


class TextMapGl(TextureGl):
    def __init__(self,name,text, font_path=r"C:\Windows\Fonts\arial.ttf", font_size=32):
        super().__init__(name,"")

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


    def get_image(self):
        """
                Create an image with Pillow containing the text.
                """
        font = ImageFont.truetype(self.font_path, self.font_size)
        text_bbox = font.getbbox(self.text)
        text_size = (text_bbox[2] - text_bbox[0], text_bbox[3])
        self.width, self.height = text_size

        # Create an RGBA image
        image = Image.new("RGBA", text_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), self.text, font=font, fill=(255, 255, 255, 255))

        img_data = np.array(image, dtype=np.uint8)
        return img_data
