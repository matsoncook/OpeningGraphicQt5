from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram

class TextMapShader:
    def __init__(self):
        VERTEX_SHADER = """
            #version 430 core
            layout(location = 0) in vec3 position;
            layout (location = 1) in vec2 aTexCoord;
            
            uniform mat4 world_matrix;
            out vec2 vLocalPos;
            void main() {
                gl_Position = world_matrix * vec4(position, 1.0);
                vTexCoord = aTexCoord;
            }
            """

        FRAGMENT_SHADER = """
             #version 330 core

            in vec2 vTexCoord;   // Interpolated texture coordinate from the vertex shader
            out vec4 FragColor;  // Final output color
            
            uniform sampler2D uTexture; // The texture sampler
            
            void main()
            {
                // Sample the texture using the texture coordinate
                FragColor = texture(uTexture, vTexCoord);
            }
                        """
        self.shader_program = compileProgram(
            compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
            compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER),
        )