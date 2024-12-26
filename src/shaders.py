from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram

class Shaders:
    def __init__(self):
        self.glowing_circle_vertex_shader = """
                   #version 330 core
                   layout(location = 0) in vec2 position;
                   //uniform vec2 circle_position;
                   void main() {
                       gl_Position = vec4(position, 0.0, 1.0);
                   }
                   """
        self.glowing_circle_fragment_shader = """
                   #version 330 core
                   out vec4 fragColor;
                   uniform vec2 resolution;
                   uniform vec2 circle_center;
                   uniform float circle_radius;
                   uniform vec3 circle_color;

                   void main() {


                       //This is setting up a -1 to 1 normalised window
                       vec2 uv = gl_FragCoord.xy / resolution;
                       vec2 p = uv * 2.0 - 1.0;


                       float dist = length(p - circle_center);


                       //float intensity = smoothstep(circle_radius, circle_radius * 0.9, dist);
                       float intensity = smoothstep(circle_radius*1.5, circle_radius * 0.8, dist);//increase glow


                       // Apply color and transparency
                       vec3 color = circle_color * intensity;
                       fragColor = vec4(color, intensity);  // Alpha is based on intensity
                   }
                   """
        self.glowing_circle_shader_program = compileProgram(
            compileShader(self.glowing_circle_vertex_shader, GL_VERTEX_SHADER),
            compileShader(self.glowing_circle_fragment_shader, GL_FRAGMENT_SHADER)
        )