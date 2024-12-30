'''


See cook books/opengl/framebuffer


'''




from OpenGL.GL import *
def main():
    # Initialize context and create a window (e.g., via PyGame)
    pygame.init()
    pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)

    # Create shaders
    scene_shader = create_scene_shader()  # Shader to render glowing line
    post_shader = create_post_shader()    # Shader for post-processing

    # Create FBO and its texture
    fbo, fbo_texture = create_framebuffer(800, 600)

    # Create objects for rendering (e.g., a glowing line VAO and a fullscreen quad)
    line_vao = create_line_vao()
    fullscreen_vao = create_fullscreen_quad()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False

        # 1. Render to FBO
        glBindFramebuffer(GL_FRAMEBUFFER, fbo)
        glViewport(0, 0, 800, 600)  # Match FBO resolution
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Use the scene shader to render a glowing line
        glUseProgram(scene_shader)
        glBindVertexArray(line_vao)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

        glBindFramebuffer(GL_FRAMEBUFFER, 0)  # Return to default framebuffer

        # 2. Render the FBO texture to the screen with post-processing
        glViewport(0, 0, 800, 600)  # Match screen resolution
        glClearColor(0.1, 0.1, 0.15, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(post_shader)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, fbo_texture)
        glUniform1i(glGetUniformLocation(post_shader, "uSceneTexture"), 0)

        glBindVertexArray(fullscreen_vao)
        glDrawArrays(GL_TRIANGLES, 0, 6)

        pygame.display.flip()

    pygame.quit()

def create_framebuffer(width, height):
    # Generate a framebuffer object (FBO)
    fbo = glGenFramebuffers(1)
    glBindFramebuffer(GL_FRAMEBUFFER, fbo)

    # Create a texture to render into
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # Attach the texture to the framebuffer
    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, texture, 0)

    # (Optional) Create a renderbuffer for depth/stencil testing
    renderbuffer = glGenRenderbuffers(1)
    glBindRenderbuffer(GL_RENDERBUFFER, renderbuffer)
    glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH24_STENCIL8, width, height)
    glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_RENDERBUFFER, renderbuffer)

    # Check if framebuffer is complete
    if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
        raise Exception("Framebuffer is not complete")

    # Unbind the framebuffer and renderbuffer
    glBindFramebuffer(GL_FRAMEBUFFER, 0)
    glBindRenderbuffer(GL_RENDERBUFFER, 0)

    return fbo, texture

def render_to_buffer():
    # Set the size of the texture (and therefore the framebuffer resolution)
    width, height = 800, 600

    # Create the framebuffer and texture
    fbo, texture = create_framebuffer(width, height)

    # Render to framebuffer
    glBindFramebuffer(GL_FRAMEBUFFER, fbo)
    glViewport(0, 0, width, height)  # Set viewport to texture size
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Perform your rendering here (e.g., draw objects to this FBO)

    glBindFramebuffer(GL_FRAMEBUFFER, 0)  # Bind the default framebuffer


def use_the_texture():
    # Bind the framebuffer texture to a shader's uniform
    glUseProgram(post_processing_shader)
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, texture)
    glUniform1i(glGetUniformLocation(post_processing_shader, "uSceneTexture"), 0)

    # Render a fullscreen quad with the texture applied
    fullscreen_vao = create_fullscreen_quad()  # A simple quad covering the screen
    glBindVertexArray(fullscreen_vao)
    glDrawArrays(GL_TRIANGLES, 0, 6)
