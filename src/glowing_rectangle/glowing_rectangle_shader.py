class GlowingRectangleShader():

    def __init__(self):

        self.glowing_rectangle_vertex_shader = """
            #version 430 core
            layout(location = 0) in vec3 position;
            
            uniform mat4 model;
            
            void main() {
                gl_Position = model * vec4(position, 1.0);
            }
            """
        self.glowing_rectangle_fragment_shader = """
            #version 430 core
            out vec4 FragColor;
            
            void main() {
                // Simple glowing effect by using alpha blending
                float glow = 0.6 + 0.4 * sin(gl_FragCoord.x * 0.05);
                FragColor = vec4(1.0, 0.5, 0.0, glow); // Orange color with a glow effect
            }
            """