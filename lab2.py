#!/usr/bin/env python3
import sys
import random
import time as time_lib

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass


# przerzutnia (przeksztalca zakres rysowania [-1.0; 1.0] -> [-100.0; 100.0]
def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()

def render(time):
    glClear(GL_COLOR_BUFFER_BIT)
    dywan(100, 100, 3, 0.2)
    glFlush()
    

def rect(x, y, a, b, color, d=0.0):
    glColor3f(color[0], color[1], color[2])
    glBegin(GL_TRIANGLE_FAN)
    a = a * (1 + d)
    x = float(x) - a/2
    y = float(y) - b/2
    glVertex2f(x,   y)
    glVertex2f(x+a, y)
    glVertex2f(x+a, y+b)
    glVertex2f(x,   y+b)
    glEnd()

def dywan(w, h, depth, d=0.0):
    black = [0.0, 0.0, 0.0]
    w *= (1 + d)
    rect(0, 0, w, h, black)
    dywan_aux(w, h, 0, 0, depth)
    
def dywan_aux(w, h, x_offset, y_offset, depth):
    if depth == 0:
        return
    white = [1.0, 1.0, 1.0]
    rect(x_offset, y_offset, w/3, h/3, white)
    dywan_aux(w/3, h/3, x_offset,      h/3+y_offset,  depth-1) #N
    dywan_aux(w/3, h/3, w/3+x_offset,  h/3+y_offset,  depth-1) #NE
    dywan_aux(w/3, h/3, w/3+x_offset,  y_offset,      depth-1) #E
    dywan_aux(w/3, h/3, w/3+x_offset,  -h/3-y_offset, depth-1) #SE
    dywan_aux(w/3, h/3, x_offset,      -h/3-y_offset, depth-1) #S
    dywan_aux(w/3, h/3, -w/3-x_offset, -h/3-y_offset, depth-1) #SW
    dywan_aux(w/3, h/3, -w/3-x_offset, y_offset,      depth-1) #W    
    dywan_aux(w/3, h/3, -w/3-x_offset, h/3+y_offset,  depth-1) #NW

def dywan_iter(w, h, depth, d=0.0):
    pass

if __name__ == '__main__':
    main()
