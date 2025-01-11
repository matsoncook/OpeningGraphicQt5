import numpy as np

from base.base_object_gl4 import BaseObjectGL4
from shaders import Shaders

from OpenGL.GL import *
from PIL import Image, ImageDraw, ImageFont
class TextureGl(BaseObjectGL4):
    def __init__(self,name,file_path):
        super().__init__(name)
        self.file_path = file_path

    def init_gl(self, shaders: Shaders):
        # Initialize shaders
        self.shader_program = shaders.texture_shader_program
        self.initializeGL()

    def get_image(self):
        # Load image using PIL
        image = Image.open(self.file_path)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)  # Flip image vertically
        img_data = np.array(image, dtype=np.uint8)
        return img_data
    def load_texture(self):


        img_data = self.get_image()
        shape = img_data.shape

        # Generate and bind texture
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        # Set texture parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # Upload texture data
        #glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, shape[1], shape[0], 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

        return texture_id
    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)



        # Vertex data (Position and Texture Coordinates)
        vertices = np.array([
            # Position      TexCoords
            -0.5, -0.5, 0.0, 0.0,  # Bottom-left
            0.5, -0.5, 1.0, 0.0,  # Bottom-right
            0.5, 0.5, 1.0, 1.0,  # Top-right
            -0.5, 0.5, 0.0, 1.0  # Top-left
        ], dtype=np.float32)

        indices = np.array([
            0, 1, 2,  # First triangle
            2, 3, 0  # Second triangle
        ], dtype=np.uint32)



        # Create VAO
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        # Create VBO
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        # Create EBO (Element Buffer Object)
        ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

        # Specify vertex attributes
        position_loc = glGetAttribLocation(self.shader_program, "aPosition")
        texcoord_loc = glGetAttribLocation(self.shader_program, "aTexCoord")
        glEnableVertexAttribArray(position_loc)
        glVertexAttribPointer(position_loc, 2, GL_FLOAT, GL_FALSE, 4 * vertices.itemsize, ctypes.c_void_p(0))
        glEnableVertexAttribArray(texcoord_loc)
        glVertexAttribPointer(texcoord_loc, 2, GL_FLOAT, GL_FALSE, 4 * vertices.itemsize,
                              ctypes.c_void_p(2 * vertices.itemsize))

        # Load texture
        self.texture_id = self.load_texture()

        # Unbind VAO
        glBindVertexArray(0)

    def paint_gl(self, context):




        # Bind texture
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glUniform1i(glGetUniformLocation(self.shader_program, "uTexture"), 0)

        # Draw the textured quad
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)