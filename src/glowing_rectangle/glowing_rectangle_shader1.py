class GlowingRectangleShader():

    def __init__(self):

        self.VERTEX_SHADER = """
            #version 430 core
            layout(location = 0) in vec3 position;
            
            uniform mat4 world_matrix;
            out vec2 vLocalPos;
            void main() {
                gl_Position = world_matrix * vec4(position, 1.0);
                vLocalPos = position.xy;
            }
            """
        self.glowing_rectangle_fragment_shader1 = """
            #version 430 core
            out vec4 FragColor;
            
            void main() {
                // Simple glowing effect by using alpha blending
                float glow = 0.6 + 0.4 * sin(gl_FragCoord.x * 0.05);
                FragColor = vec4(1.0, 0.5, 0.0, glow); // Orange color with a glow effect
            }
            """

        self.FRAGMENT_SHADER = """
        #version 330 core

        in vec2 vLocalPos;
        out vec4 FragColor;

        uniform vec3 uColor;      // Base color of the line
        uniform float uGlowWidth; // Controls the glow radius
        uniform float uGlowSoft;  // Controls how soft the glow falls off

        void main()
        {
            // Distance from the center line (which is y=0)
            float dist = abs(vLocalPos.y);

            // We can use a smooth exponential or simple linear fade:
            // e.g. alpha = exp(-dist * uGlowSoft) if dist < uGlowWidth
            // or 0 if dist > uGlowWidth.

            if (dist > uGlowWidth)
            {
                // Outside the glow region -> fully transparent
                discard;  // or FragColor = vec4(0.0);
            }

            // Exponential fade
            float alpha = exp(-dist * uGlowSoft);

            FragColor = vec4(uColor, alpha);
        }
        """;