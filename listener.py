from classes.controller import TurtleController
import matplotlib.pyplot as plt
from classes.turtle import Turtle
from OpenGL.GL import *
import numpy as np
import random
import glfw
import time
import glm
import sys

def render(turtles):
    glClearColor(0.3, 0.3, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    for turtle in turtles:
        transform = glm.rotate(glm.translate(glm.mat4(1.0), glm.vec3(turtle.get_position(), 0.0)), turtle.position.z, glm.vec3(0.0, 0.0, 1.0))
        glUniformMatrix4fv(0, 1, 0, glm.value_ptr(transform))
        glUniform3fv(1, 1, glm.value_ptr(turtle.color))
        glDrawArrays(GL_TRIANGLES, 0, 6)

def step_sim(keyboard, turtles):
    keyboard.update()
    for turtle in turtles:
        turtle.chase()

if __name__ == "__main__":
    if not glfw.init():
        print('init error')
        sys.exit(1)

    window = glfw.create_window(600, 600, "TurtleSim", None, None)
    glfw.make_context_current(window)
    glViewport(0, 0, 600, 600)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    commander = Turtle('turtle1')
    controls = TurtleController(commander)

    turtles = [ commander ]
    num_turtles = 5
    if len(sys.argv) > 1:
        num_turtles = int(sys.argv[1])
    for i in range(2, 2 + num_turtles):
       turtle = Turtle('turtle'+str(i), 'turtle'+str(i-1))
       turtle.set_position(glm.vec2(random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)))
       turtles.append(turtle)

    program = glCreateProgram()

    vert = glCreateShader(GL_VERTEX_SHADER)
    frag = glCreateShader(GL_FRAGMENT_SHADER)
    vert_source = open("shaders/shader.vert", "r")
    frag_source = open("shaders/shader.frag", "r")

    glShaderSource(vert, vert_source)
    glShaderSource(frag, frag_source)
    glCompileShader(vert)
    glCompileShader(frag)

    if (glGetShaderiv(vert, GL_COMPILE_STATUS) == 0):
        print('Vertex shader compile error ', glGetShaderInfoLog(vert))

    if (glGetShaderiv(frag, GL_COMPILE_STATUS) == 0):
        print('Fragment shader compile error: ', glGetShaderInfoLog(frag))

    glAttachShader(program, vert)
    glAttachShader(program, frag)
    glLinkProgram(program)
    glUseProgram(program)
    
    glDeleteShader(vert)
    glDeleteShader(frag)
    vert_source.close()
    frag_source.close()

    tex = glGenTextures(1)
    image = np.array(plt.imread('assets/turtle.png') * 255.0, dtype=np.ubyte) 
    glBindTexture(GL_TEXTURE_2D, tex)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.shape[0], image.shape[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    glGenerateMipmap(GL_TEXTURE_2D)

    freq = 1.0 / 30.0
    while not glfw.window_should_close(window):
        start = time.time()
        glfw.poll_events()
        step_sim(controls, turtles)
        render(turtles)
        glfw.swap_buffers(window)
        while time.time() - start < freq:
            pass

    glDeleteProgram(program)
    glfw.terminate()