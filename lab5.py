#!/usr/bin/env python3
import sys
import numpy as np
from math import sin, cos, pi, pow, sqrt

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

viewer = [0.0, 0.0, 15.0]

theta = 0.0
phi = 0.0
pix2angle = 1.0
angle2radian = 0.017453292519943295

space, shift, x, y, z = False, False, False, False, False

left_mouse_button_pressed = 0
mouse_x_pos_old = 0.0
delta_x = 0.0
mouse_y_pos_old = 0.0
delta_y = 0.0
moved = False

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.1, 1.0]
light_diffuse = [0.8, 0.8, 0.8, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

light_ambient_1 = [0.1, 0.1, 0.0, 1.0]
light_diffuse_1 = [0.8, 0.0, 0.8, 1.0]
light_specular_1 = [1.0, 1.0, 1.0, 1.0]
light_position_1 = [0.0, 10.0, 0.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    # material
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    # light0
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    # light1
    glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient_1)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse_1)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular_1)
    glLightfv(GL_LIGHT1, GL_POSITION, light_position_1)

    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att_quadratic)

    # enable light
    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    # glEnable(GL_LIGHT1)


def shutdown():
    pass

def move_light():
    global theta, phi
    global light_position
    global moved
    global shift, x, y, z
    # if moved:
    #     theta += delta_x * pix2angle / 10
    #     phi += delta_y * pix2angle / 10
    #     moved = False

    # R = 10
    # light_position[0] = R * cos(theta) * cos(phi)
    # light_position[1] = R * sin(phi)
    # light_position[2] = R * sin(theta) * cos(phi)
    # xs, zs, ys, _ = light_position

    # light moving x, y, z | shift is reversing
    speed = 0.5 - 1*shift
    if x:
        light_position[0] += speed
    if y:
        light_position[1] += speed
    if z:
        light_position[2] += speed
    xs, zs, ys, _ = light_position
    
    # paint camera
    glTranslate(xs, ys, zs)
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 0.5, 6, 5)
    gluDeleteQuadric(quadric)
    glTranslate(-xs, -ys, -zs)
    
    glLightfv(GL_LIGHT0, GL_POSITION, np.add(light_position, viewer+[0]))

def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()



def keyboard_key_callback(window, key, scancode, action, mods):
    global space
    global x, y, z, shift
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    if key == GLFW_KEY_SPACE and action == GLFW_PRESS:
        space = True
    # x
    if key == GLFW_KEY_X and action == GLFW_PRESS:
        x = True
    if key == GLFW_KEY_X and action == GLFW_RELEASE:
        x = False

    # y
    if key == GLFW_KEY_Y and action == GLFW_PRESS:
        y = True
    if key == GLFW_KEY_Y and action == GLFW_RELEASE:
        y = False

    # z
    if key == GLFW_KEY_Z and action == GLFW_PRESS:
        z = True
    if key == GLFW_KEY_Z and action == GLFW_RELEASE:
        z = False

    # shift
    if key == GLFW_KEY_LEFT_SHIFT and action == GLFW_PRESS:
        shift = True
    if key == GLFW_KEY_LEFT_SHIFT and action == GLFW_RELEASE:
        shift = False
    


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global delta_y
    global mouse_x_pos_old
    global mouse_y_pos_old
    global moved
    
    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos
    
    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos
    
    moved = True


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0

def take_and_eval():
    global light_ambient, light_diffuse, light_specular
    global space
    a = light_ambient
    d = light_diffuse
    s = light_specular
    instruction = input("give instruction:\na(mbient), d(iffuse), s(pecular), [0/1/2] = (0.0-1.0)\n")
    if instruction.strip() == "quit":
        print("quitted successfully")
        space = False
        return
    exec(instruction)
    glLightfv(GL_LIGHT0, GL_AMBIENT, a)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, d)
    glLightfv(GL_LIGHT0, GL_SPECULAR, s)
    print("ambient: ", glGetLightfv(GL_LIGHT0, GL_AMBIENT))
    print("diffuse: ", glGetLightfv(GL_LIGHT0, GL_DIFFUSE))
    print("specular: ", glGetLightfv(GL_LIGHT0, GL_SPECULAR))
    print()

    
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

    tab, normal = get_coordinates(10)

    startup()
    while not glfwWindowShouldClose(window):
        if space:
            take_and_eval()
        render(glfwGetTime(), tab, normal)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()

    
def render(time, tab, normal):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    angle = time * 180 / 3.1415
    glRotatef(angle, 1.0, 0.5, 0.5)
    render_object(tab, normal)
    glRotatef(-angle, 1.0, 0.5, 0.5)
    move_light()
    glFlush()

def spin(angle):
        glRotatef(angle, 1.0, 0.0, 0.0)
        glRotatef(angle, 0.0, 1.0, 0.0)
        glRotatef(angle, 0.0, 0.0, 1.0)



def render_object(tab, normal):
    egg_triangle_strip(tab, normal)
    # quadric = gluNewQuadric()
    # gluQuadricDrawStyle(quadric, GLU_FILL)
    # gluSphere(quadric, 3.0, 10, 10)
    # gluDeleteQuadric(quadric)

def n(u, v):
    def xdu(u, v):
        return (-450 * pow(u, 4) + 900 * pow(u, 3) - 810 * pow(u, 2) + 360 * u - 45) * cos(pi * v)
    def xdv(u, v):
        return pi * (90 * pow(u, 5) - 225 * pow(u, 4) + 270 * pow(u, 3) - 180 * pow(u, 2) + 45 * u) * sin(pi * v)

    def ydu(u, v):
        return 640 * pow(u, 3) - 960 * pow(u, 2) + 320 * u

    def ydv(u, v):
        return 0

    def zdu(u, v):
        return (-450 * pow(u, 4) + 900 * pow(u, 3) - 810 * pow(u, 2) + 360 * u - 45) * sin(pi * v)

    def zdv(u, v):
        return - pi * (90 * pow(u, 5) - 225 * pow(u, 4) + 270 * pow(u, 3) - 180 * pow(u, 2) + 45 * u) * cos(pi * v)
    
    xu = xdu(u, v)
    xv = xdv(u, v)
    yu = ydu(u, v)
    yv = ydv(u, v)
    zu = zdu(u, v)
    zv = zdv(u, v)

    def normalize_vector(vector):
        magnitude = np.linalg.norm(vector)
        if magnitude == 0:
            return vector  # Avoid division by zero
        return vector / magnitude
    a = 1
    if u > 0.5:
        a = -1
    return normalize_vector([yu*zv-zu*yv,
                             zu*xv-xu*zv,
                             xu*yv-yu*xv]) * a



def get_coordinates(N):
    tab = [[[0] * 3 for i in range(N)] for j in range(N)]
    normal = [[[0] * 3 for i in range(N)] for j in range(N)]
    u_args = []
    v_args = []
    for i in range(N):
        u_args.append(i/N)
        v_args.append(i/N)
    for idx_u, u in enumerate(u_args):
        for idx_v, v in enumerate(v_args):
            x = (-90*(u**5) + 225*(u**4) - 270*(u**3) + 180*(u**2) - 45*u) * cos(pi * v)
            y = 160*(u**4) - 320*(u**3) + 160*(u**2) - 5
            z = (-90*(u**5) + 225*(u**4) - 270*(u**3) + 180*(u**2) - 45*u) * sin(pi * v)
            tab[idx_u][idx_v][0] = x
            tab[idx_u][idx_v][1] = y
            tab[idx_u][idx_v][2] = z
            normal[idx_u][idx_v] = n(u, v)
    return (tab, normal)

def build_drawer(tab, normal):
    def draw_normal(i, j):
        glBegin(GL_LINES)
        glVertex3fv(tab[i][j])
        end = np.add(tab[i][j], normal[i][j])
        glVertex3fv(end)
        glEnd()
    return draw_normal
    
def egg_triangle_strip(tab, normal):
    N = len(tab)
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(N):
        for j in range(N):
            if i==0:
                glNormal3fv(normal[i][j])
                glVertex3fv(tab[i][j])
                glNormal3fv(normal[i+1][j])
                glVertex3fv(tab[i+1][j])
                if j+1==N:
                    glNormal3fv(normal[N-1][0])
                    glVertex3fv(tab[N-1][0])
                else:
                    glNormal3fv(normal[i+1][j+1])
                    glVertex3fv(tab[i+1][j+1])
            elif i==N-1:
                glNormal3fv(normal[i][j])
                glVertex3fv(tab[i][j])
                glNormal3fv(normal[0][0])
                glVertex3fv(tab[0][0])
                if j+1==N:
                    glNormal3fv(normal[1][0])
                    glVertex3fv(tab[1][0])
                else:
                    glNormal3fv(normal[i][j+1])
                    glVertex3fv(tab[i][j+1])
            else:
                if j+1==N:
                    glNormal3fv(normal[i][j])
                    glVertex3fv(tab[i][j])
                    glNormal3fv(normal[i+1][j])
                    glVertex3fv(tab[i+1][j])
                    glNormal3fv(normal[N-i][0])
                    glVertex3fv(tab[N-i][0])
                    glNormal3fv(normal[N-(i+1)][0])
                    glVertex3fv(tab[N-(i+1)][0])
                    continue
                glNormal3fv(normal[i][j])
                glVertex3fv(tab[i][j])
                glNormal3fv(normal[i+1][j])
                glVertex3fv(tab[i+1][j])
                glNormal3fv(normal[i][j+1])
                glVertex3fv(tab[i][j+1])
                glNormal3fv(normal[i+1][j+1])
                glVertex3fv(tab[i+1][j+1])
    glEnd()
    
    drawer = build_drawer(tab, normal)
    for i in range(N):
        for j in range(N):
            if i==0:
                drawer(i, j)
                drawer(i+1, j)
                if j+1==N:
                    drawer(N-1, 0)
                else:
                    drawer(N-1, 0)
            elif i==N-1:
                drawer(i, j)
                drawer(0, 0)
                if j+1==N:
                    drawer(1, 0)
                else:
                    drawer(i, j+1)
            else:
                if j+1==N:
                    drawer(i, j)
                    drawer(i+1, j)
                    drawer(N-i, 0)
                    drawer(N-(i+1), 0)
                    continue
                drawer(i, j)
                drawer(i+1, j)
                drawer(i, j+1)
                drawer(i+1, j+1)
    glBegin(GL_LINES)
    bottom = tab[0][0]
    glNormal3fv([0, -1, 0])
    glVertex3fv(bottom)
    glVertex3f(bottom[0], bottom[1] - 1, bottom[2])
    top = tab[int(N/2)][0]
    glNormal3fv([0, 1, 0])
    glVertex3fv(top)
    glVertex3f(top[0], top[1] + 1, top[2])
    glEnd()

if __name__ == '__main__':
    main()
