#!/usr/bin/env python3
import sys
import math
import numpy as np

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

def rotation_matrix(angle, axis):
    x, y, z = axis / np.linalg.norm(axis)
    cos_theta = np.cos(angle)
    sin_theta = np.sin(angle)
    one_minus_cos_theta = 1 - cos_theta

    matrix = np.array([
        [cos_theta + x**2 * one_minus_cos_theta,     x * y * one_minus_cos_theta - z * sin_theta,     x * z * one_minus_cos_theta + y * sin_theta],
        [y * x * one_minus_cos_theta + z * sin_theta, cos_theta + y**2 * one_minus_cos_theta,         y * z * one_minus_cos_theta - x * sin_theta],
        [z * x * one_minus_cos_theta - y * sin_theta, z * y * one_minus_cos_theta + x * sin_theta,     cos_theta + z**2 * one_minus_cos_theta]
    ])

    return matrix

def rotate_vector(angle, axis, vector):
    angle = np.radians(angle)
    # Compute the rotation matrix
    r_matrix = rotation_matrix(angle, axis)

    # Perform the rotation using np.dot (matrix-vector multiplication)
    rotated_vector = np.dot(r_matrix, vector)

    # Limit the vector to two decimal places

    return rotated_vector



viewer = [0.0, 0.0, 10.0]

margin = 0

theta = 0.0
phi = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0

R = 5
R_inc = 0.05
right_mouse_button_pressed = 0
scale = 5
scale_inc = 0.05

mouse_y_pos_old = 0
delta_y = 0

w_pressed = False
a_pressed = False
s_pressed = False
d_pressed = False

x = 5
y = 0
z = 0

start_direction = [-1, 0, 0]
view_direction = start_direction

up =     [0, 1, 0]

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


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


def example_object():
    glColor3f(1.0, 1.0, 1.0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    glRotatef(90, 1.0, 0.0, 0.0)
    glRotatef(-90, 0.0, 1.0, 0.0)

    gluSphere(quadric, 1.5, 10, 10)

    glTranslatef(0.0, 0.0, 1.1)
    gluCylinder(quadric, 1.0, 1.5, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, -1.1)

    glTranslatef(0.0, 0.0, -2.6)
    gluCylinder(quadric, 0.0, 1.0, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, 2.6)

    glRotatef(90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(-90, 1.0, 0.0, 1.0)

    glRotatef(-90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(90, 1.0, 0.0, 1.0)

    glRotatef(90, 0.0, 1.0, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    gluDeleteQuadric(quadric)

def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    #move_camera()
    #move_object()
    move_gaming()

    axes()
    example_object()
    glFlush()

def delete_last_lines(n=1):
        CURSOR_UP_ONE = '\x1b[1A' 
        ERASE_LINE = '\x1b[2K' 
        for _ in range(n): 
            sys.stdout.write(CURSOR_UP_ONE) 
            sys.stdout.write(ERASE_LINE)

def move_gaming():    
    global R
    global R_inc
    global w_pressed
    global a_pressed
    global s_pressed
    global d_pressed
    global x
    global y
    global z
    global up
    
    if right_mouse_button_pressed:
        if (int(R) == 5 or int(R) == 0):
            R_inc = - R_inc
        R += R_inc
        
    eye =    [x, y, z]
    center = [0, 0, 0]

    if w_pressed:
        x += view_direction[0]/10
        y += view_direction[1]/10
        z += view_direction[2]/10
    if s_pressed:
        x -= view_direction[0]/10
        y -= view_direction[1]/10
        z -= view_direction[2]/10

    h = np.cross(up, view_direction) # a and d
    if a_pressed:
        x += h[0]/10
        y += h[1]/10
        z += h[2]/10
    if d_pressed:
        x -= h[0]/10
        y -= h[1]/10
        z -= h[2]/10
        
    
    gluLookAt(eye[0],     eye[1],    eye[2],
              eye[0]+view_direction[0], eye[1]+view_direction[1], eye[2]+view_direction[2],
              up[0],     up[1],     up[2])

    # debug
    # print(f'width: {width}, height: {height}, upX: {upX:.2f}, upY: {upY:.2f},  upZ: {upZ:.2f}')
    # print(f'x,y,z_eye: [{eye[0]:.2f}, {eye[1]:.2f}, {eye[2]:.2f}]')
    # print(f'theta: {theta%360:.0f}')
    # delete_last_lines(2)

def move_object():
    global theta
    global phi
    global scale
    global scale_inc
    global left_mouse_button_pressed
    global right_mouse_button_pressed
    global viewer

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    
    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle
                
    if right_mouse_button_pressed:
        if (int(scale) == 5 or int(scale) == 0):
            scale_inc = - scale_inc
        scale += scale_inc
        
    glScalef(scale, scale, scale)
    glRotate(theta, 0.0, 1.0, 0.0)
    glRotate(phi,   1.0, 0.0, 0.0)


def move_camera():
    global theta
    global phi
    global R
    global R_inc
    global viewer
    if left_mouse_button_pressed:
        phi += delta_y * pix2angle
        phi %= 360
        theta += delta_x * pix2angle
        theta %= 360

    if right_mouse_button_pressed:
        if (int(R) == 5 or int(R) == 0):
            R_inc = - R_inc
        R += R_inc

    theta_scaled = theta * (math.pi / 180)
    phi_scaled = phi * (math.pi / 180)
    
    x_eye = R * math.cos(theta_scaled) * math.cos(phi_scaled)
    y_eye = R * math.sin(phi_scaled)
    z_eye = R * math.sin(theta_scaled) * math.cos(phi_scaled)
    viewer = [x_eye, y_eye, z_eye]
    upY = 1 - 2 * (phi > 90 and phi <= 270)        
    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, upY, 0.0)

    # debug
    # print(f'x,y,z_eye: [{viewer[0]:.2f}, {viewer[1]:.2f}, {viewer[2]:.2f}]')
    # print(f'theta: {theta%360:.0f}')
    # delete_last_lines(2)
    
    


def update_viewport(window, width, height):
    global pix2angle
    global margin
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    margin = int(math.fabs(height - width) / 2)

    if width <= height:
        glViewport(0, margin, width, width)
    else:
        glViewport(margin, 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    global w_pressed
    global a_pressed
    global s_pressed
    global d_pressed
    
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    if key == GLFW_KEY_W:
        w_pressed = action == GLFW_PRESS or action != GLFW_RELEASE
    if key == GLFW_KEY_A:
        a_pressed = action == GLFW_PRESS or action != GLFW_RELEASE
    if key == GLFW_KEY_S:
        s_pressed = action == GLFW_PRESS or action != GLFW_RELEASE
    if key == GLFW_KEY_D:
        d_pressed = action == GLFW_PRESS or action != GLFW_RELEASE


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global delta_y
    global mouse_x_pos_old
    global mouse_y_pos_old
    global view_direction
    global start_direction
    global up
    # global mouse_position
    # global old_mouse_position

    # old_mouse_position = mouse_position
    *_, width, height = glGetIntegerv(GL_VIEWPORT)
    # if width >= height:
    #     mouse_position = [max(min(x_pos - margin, width), 0), y_pos]
    # else:
    #     mouse_position = [x_pos, max(min(y_pos - margin, height), 0)]
    # mX = (mouse_position[0] - (width/2)) / (width/2)
    # mY = (mouse_position[1] - (height/2)) / (height/2)
    # mouse_position = [mX, mY]
    
    delta_x = x_pos - mouse_x_pos_old
   

    delta_y = y_pos - mouse_y_pos_old
    


    old_angleX = -270*(mouse_x_pos_old-(width/2))/(width/2)
    old_angleY = 120*(mouse_y_pos_old-(height/2))/(height/2)
    
    angleX = -270*(x_pos-(width/2))/(width/2)
    angleY = 120*(y_pos-(height/2))/(height/2)

    dAX = angleX - old_angleX
    dAY = angleY - old_angleY

    if dAY > 15 or dAX > 15:
        dAY = 0
        dAX = 0
    # angleX = -180*(delta_x/width)
    # angleY = 90*(delta_y/height)
    # if delta_x > 15:
    #     angleX = 0
    # if delta_y > 15:
    #     angleY = 0

    # print(delta_y)

    h = np.cross(up, view_direction)
    view_direction = rotate_vector(dAX, up, view_direction)
    view_direction = rotate_vector(dAY, h, view_direction)
    
    mouse_x_pos_old = x_pos
    mouse_y_pos_old = y_pos
    #view_direction = [r[0] * view_direction[0],
    #                  r[1] * view_direction[1],
    #                  r[2] * view_direction[2]] 

    
def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed
    global right_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0

    right_mouse_button_pressed = \
        button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS

def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
