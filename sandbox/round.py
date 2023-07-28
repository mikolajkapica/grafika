#!/usr/bin/env python3
import sys
import random
import time as time_lib
from math import cos, sin, pi

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
    drawRoundedRectangle(-50, 50, 100, 100, 10)
    glFlush()
    

def drawRoundedCorner(centerX, centerY, radius, numSegments, rotation=0.0):
    rotation = rotation / 180.0 * pi
    for i in range(numSegments):
        angle = i / numSegments * 3.14159265358979323846 * 0.5
        angle += rotation
        x = centerX + radius * sin(angle)
        y = centerY + radius * cos(angle)
        glVertex2f(x, y)

def drawRoundedRectangle(x, y, a, b, r):
    glBegin(GL_TRIANGLE_FAN)
    drawRoundedCorner(x + r, y - r, r,         20, -90)
    drawRoundedCorner(x + a - r, y - r, r,     20, 0)
    drawRoundedCorner(x + a - r, y - b + r, r, 20, 90)
    drawRoundedCorner(x + r, y - b + r, r,     20, 180)
    glEnd()

if __name__ == '__main__':
    main()
