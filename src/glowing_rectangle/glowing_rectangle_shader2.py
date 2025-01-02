class GlowingRectangleShader():

    def __init__(self):

        self.VERTEX_SHADER = """
            #version 430 core
            
            layout(location = 0) in vec3 aPosition;
            
            uniform mat4 world_matrix;
            out vec3 vPosition;
            
            void main() {
                gl_Position = world_matrix * vec4(aPosition, 1.0);
                vPosition = aPosition;
            }
            """
        self.distancetoline= '''
            float pointToLineDistance(vec3 point, vec3 linePoint, vec3 lineDirection) {
                // Vector from linePoint to point
                vec3 lineToPoint = point - linePoint;
            
                // Cross product of the vector to the point and the line's direction
                vec3 crossProduct = cross(lineToPoint, lineDirection);
            
                // Magnitude of the cross product
                float crossMagnitude = length(crossProduct);
            
                // Magnitude of the line's direction vector
                float directionMagnitude = length(lineDirection);
            
                // Perpendicular distance
                return crossMagnitude / directionMagnitude;
            }
        '''
        self.FRAGMENT_SHADER = """
            #version 430 core
            out vec4 FragColor;
            in vec3 vPosition;
            
            void main() {
                float dist =  abs(vPosition.y);
                // Simple glowing effect by using alpha blending
                float intensity = smoothstep(0.05, 0.0, dist);//increase glow

                FragColor = vec4(1.0, 1.0, 1.0, intensity); // Orange color with a glow effect
            }
            """