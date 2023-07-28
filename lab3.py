#!/usr/bin/env python3
import sys
import math
from random import random

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

def startup(N):
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    return random_colors(N)


def shutdown():
    pass


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()


def render(time, N, colors):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
#    time = 13.5
    spin(time * 180 / 3.1415)
    axes()
    #egg_lines()
    #egg_vertices()
    #egg_triangles(N, colors)
    egg_triangle_strip(N, colors)
    glFlush()


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
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

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

    N = 35
    colors = startup(N)
    while not glfwWindowShouldClose(window):
        render(glfwGetTime(), N, colors)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()

def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)

def egg_vertices():
    N = 30
    glColor3f(1.0, 1.0, 1.0)
    tab = [[[0] * 3 for i in range(N)] for j in range(N)]
    u_args = []
    v_args = []
    for i in range(N):
        u_args.append(i/N)
        v_args.append(i/N)
    for idx_u, u in enumerate(u_args):
        for idx_v, v in enumerate(v_args):
            x = (-90*(u**5) + 225*(u**4) - 270*(u**3) + 180*(u**2) - 45*u) * math.cos(math.pi * v)
            y = 160*(u**4) - 320*(u**3) + 160*(u**2) - 5
            z = (-90*(u**5) + 225*(u**4) - 270*(u**3) + 180*(u**2) - 45*u) * math.sin(math.pi * v)
            tab[idx_u][idx_v][0] = x
            tab[idx_u][idx_v][1] = y
            tab[idx_u][idx_v][2] = z
    glBegin(GL_POINTS)
    for i in range(N):
        for j in range(N):
            glColor3f(j/N, j/N, j/N)
            v = tab[i][j]
            glVertex(v[0], v[1], v[2])
    glEnd()

def egg_lines():
    N = 30
    glColor3f(1.0, 1.0, 1.0)
    tab = [[[0] * 3 for i in range(N)] for j in range(N)]
    u_args = []
    v_args = []
    for i in range(N):
        u_args.append(i/N)
        v_args.append(i/N)
    for idx_u, u in enumerate(u_args):
        for idx_v, v in enumerate(v_args):
            x = (-90*(u**5) + 225*(u**4) - 270*(u**3) + 180*(u**2) - 45*u) * math.cos(math.pi * v)
            y = 160*(u**4) - 320*(u**3) + 160*(u**2) - 5
            z = (-90*(u**5) + 225*(u**4) - 270*(u**3) + 180*(u**2) - 45*u) * math.sin(math.pi * v)
            tab[idx_u][idx_v][0] = x
            tab[idx_u][idx_v][1] = y
            tab[idx_u][idx_v][2] = z
    glBegin(GL_LINES)
    for i in range(N):
        for j in range(N):
            # vertical lines
            v = tab[i][j]
            vu = tab[0][j]
            if i != N-1:
                vu = tab[i+1][j]
            glVertex(v[0], v[1], v[2])
            glVertex(vu[0], vu[1], vu[2])

            # horizontal lines
            vr = tab[i][j]
            if j != N-1:
                vr = tab[i][j+1]
            elif i != 0:
                    vr = tab[N-i][0]
            glVertex(v[0], v[1], v[2])
            glVertex(vr[0], vr[1], vr[2])
    glEnd()

def random_colors(N):
    colors = [[[0] * 3 for i in range(N)] for j in range(N)]
    for i in range(N):
        for j in range(N):
            colors[i][j] = [random(), random(), random()]
    return colors
            
def color(i, j, colors):
    glColor3fv(colors[i][j])

def egg_triangles(N, colors):
    glColor3f(1.0, 1.0, 1.0)
    tab = [[[0] * 3 for i in range(N)] for j in range(N)]
    u_args = []
    v_args = []
    for i in range(N):
        u_args.append(i/N)
        v_args.append(i/N)
    for idx_u, u in enumerate(u_args):
        for idx_v, v in enumerate(v_args):
            x = (-90*(u**5) + 225*(u**4) - 270*(u**3) + 180*(u**2) - 45*u) * math.cos(math.pi * v)
            y = 160*(u**4) - 320*(u**3) + 160*(u**2) - 5
            z = (-90*(u**5) + 225*(u**4) - 270*(u**3) + 180*(u**2) - 45*u) * math.sin(math.pi * v)
            tab[idx_u][idx_v][0] = x
            tab[idx_u][idx_v][1] = y
            tab[idx_u][idx_v][2] = z
    glBegin(GL_TRIANGLES)
    for i in range(N):
        for j in range(N):
            v = tab[i][j]
            if i+1 != N:
                vi = tab[i+1][j]
            if j+1 != N:
                vj = tab[i][j+1] 
            if i+1 != N and j+1 != N:
                vij = tab[i+1][j+1]
                color(i, j, colors)
                glVertex3fv(v)
                color(i+1, j, colors)
                glVertex3fv(vi)
                color(i, j+1, colors)
                glVertex3fv(vj)
                glVertex3fv(vj)
                color(i+1, j+1, colors)
                glVertex3fv(vij)
                color(i+1, j, colors)
                glVertex3fv(vi)
            elif i+1 == N and j+1 != N:
                color(i, j, colors)
                glVertex3fv(v)
                color(0, j, colors)
                glVertex3fv(tab[0][j])
                color(i, j+1, colors)
                glVertex3fv(vj)
                glVertex3fv(vj)
                color(0, j+1, colors)
                glVertex3fv(tab[0][j+1])
                color(0, j, colors)
                glVertex3fv(tab[0][j])
            elif i+1 != N and j+1 == N:
                if i == 0:
                    continue
                vr = tab[N-i][0]
                vri = tab[N-(i+1)][0]
                color(i, j, colors)
                glVertex3fv(v)
                
                color(N-i, 0, colors)
                glVertex3fv(vr)
                
                color(i+1, j, colors)
                glVertex3fv(vi)
                glVertex3fv(vi)
                
                color(N-i, 0, colors)
                glVertex3fv(vr)
                
                color(N-(i+1), 0, colors)
                glVertex3fv(vri)
            else:
                color(i, j, colors)
                glVertex3fv(tab[i][j])
                color(0, 0, colors)
                glVertex3fv(tab[0][0])
                color(1, 0, colors)
                glVertex3fv(tab[1][0])
                color(0, 0, colors)
                glVertex3fv(tab[0][0])
                color(i, 0, colors)
                glVertex3fv(tab[i][0])
                color(1, j, colors)
                glVertex3fv(tab[1][j])
    glEnd()
    
def egg_triangle_strip(N, colors):
    glColor3f(1.0, 1.0, 1.0)
    tab = [[[0] * 3 for i in range(N)] for j in range(N)]
    u_args = []
    v_args = []
    for i in range(N):
        u_args.append(i/N)
        v_args.append(i/N)
    for idx_u, u in enumerate(u_args):
        for idx_v, v in enumerate(v_args):
            x = (-90*(u**5) + 225*(u**4) - 270*(u**3) + 180*(u**2) - 45*u) * math.cos(math.pi * v)
            y = 160*(u**4) - 320*(u**3) + 160*(u**2) - 5
            z = (-90*(u**5) + 225*(u**4) - 270*(u**3) + 180*(u**2) - 45*u) * math.sin(math.pi * v)
            tab[idx_u][idx_v][0] = x
            tab[idx_u][idx_v][1] = y
            tab[idx_u][idx_v][2] = z
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(N):
        for j in range(N):
            glColor3f(1, 1, 1)
            if i==0:
                color(i, j, colors)
                glVertex3fv(tab[i][j])
                color(i+1, j, colors)
                glVertex3fv(tab[i+1][j])
                if j+1==N:
                    color(N-1, 0, colors)
                    glVertex3fv(tab[N-1][0])
                else:
                    color(i+1, j+1, colors)
                    glVertex3fv(tab[i+1][j+1])
            elif i==N-1:
                color(i, j, colors)
                glVertex3fv(tab[i][j])
                color(0, 0, colors)
                glVertex3fv(tab[0][0])
                if j+1==N:
                    color(1, 0, colors)
                    glVertex3fv(tab[1][0])
                else:
                    color(i, j+1, colors)
                    glVertex3fv(tab[i][j+1])
            else:
                if j+1==N:
                    color(i, j, colors)
                    glVertex3fv(tab[i][j])
                    color(i+1, j, colors)
                    glVertex3fv(tab[i+1][j])
                    color(N-i, 0, colors)
                    glVertex3fv(tab[N-i][0])
                    color(N-(i+1), 0, colors)
                    glVertex3fv(tab[N-(i+1)][0])
                    continue
                color(i, j, colors)
                glVertex3fv(tab[i][j])
                color(i+1, j, colors)
                glVertex3fv(tab[i+1][j])
                color(i, j+1, colors)
                glVertex3fv(tab[i][j+1])
                color(i+1, j+1, colors)
                glVertex3fv(tab[i+1][j+1])
    glEnd()
    

if __name__ == '__main__':
    main()
