class GlowingCircleShader:
    def __init__(self):
        self.glowing_circle_vertex_shader = """
                           #version 330 core
                           layout(location = 0) in vec3 position;
                           uniform mat4 world_matrix;
                           void main() {
                               gl_Position = world_matrix * vec4(position, 1.0);
                           }
                           """

        self.glowing_circle_fragment_shader1 = """
                       #version 330
                       out vec4 FragColor;
                       void main() {
                           FragColor = vec4(1.0, 0.5, 0.2, 1.0);
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