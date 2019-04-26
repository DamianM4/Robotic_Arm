import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from math_ik import math
from file1 import File1
from pygame.math import *
from math import fabs
import uart

WIDTH = 800
HEIGHT = 600

# defines vertices of ground in coordinate system: (z,x,y) [a bit way-out]
# it is tuple not list! it's immutable
ground_vertices = (
    (1000, 1000, 0),
    (1000, -1000, 0),
    (-1000, -1000, 0),
    (-1000, 1000, 0)
    )

# it will be fed in Values() function by txt file
arm_vertices = []


def ground():
    glBegin(GL_QUADS)
    for vertex in ground_vertices:
        glColor3fv((0.58, 0.47, 0.36))
        glVertex3fv(vertex)
    glEnd()
    glBegin(GL_LINES)
    for vertex in ground_vertices:
        glColor3fv((0.1, 0.87, 0.36))
        glVertex3fv(vertex)
    glEnd()


def arms(r):
    values(r)
    glBegin(GL_LINE_STRIP)
    glColor3fv((0.37, 0.62, 0.69))
    for i in range(4):
        glVertex3f(arm_vertices[3*i], arm_vertices[3*i+1], arm_vertices[3*i+2])
    glEnd()


def values(r):
    measure = File1().read_file_arm()
    coordinates = math().position(r[0], r[1], measure)
    # cunning use of iteration, doesn't work if is made forward,
    # adding zeros as z coordinate
    for i in reversed(range(4)):
        coordinates.insert(i*2, 0)
    for x in range(len(coordinates)):
        arm_vertices.insert(x, coordinates[x])
    '''
    for x in range(len(coordinates)):
        print(arm_vertices[x])
    '''


'''
def Normal_vect():
    v1 = Vector3(arm_vertices[3]-arm_vertices[0],arm_vertices[4]-arm_vertices[1],arm_vertices[5]-arm_vertices[2])
    v2 = Vector3(arm_vertices[6]-arm_vertices[3],arm_vertices[7]-arm_vertices[4],arm_vertices[8]-arm_vertices[5])
    vn = Vector3.cross(v1, v2)
    Vector3.normalize_ip(vn)
    for i in range(len(vn)):
        vn[i] *= 30
    return vn

def Perpendicular():
    x = glGetDoublev(GL_MODELVIEW_MATRIX)
    camera_z = x[3][0]
    camera_x = x[3][1]
    camera_y = x[3][2]
    nv = Normal_vect()
    translation_v = [camera_z-nv[0],camera_x-nv[1],camera_y-nv[2]]
    return translation_v
'''


def set_mouse_input(mx, my):
    coor = pygame.mouse.get_pos()
    mx = (coor[0] - WIDTH/2.)*2.88
    my = (-(coor[1] - HEIGHT/2.))*2.88
    r = [mx, my]
    return r


def send_to_stm(milis):
    dane=['1500', str(int(milis[0])),str(int(milis[1])), str(int(milis[2])), '1500', '1500']#in ASCI code
    # dane = ['1500', '2000', '2000', '1590', '1500', '1500']
    print("Data:")
    print (dane)
    for i in range(6):
        uart.send_data(dane[i])
    uart.receive_data()


def milisec(r):
    milis = [1500, 1500, 1500]
    measure = File1().read_file_arm()
    angles = math().position_angles(r[0], r[1], measure)
    print(angles)
    # 1st -11ms
    milis[0] = 1100+fabs(angles[0]*9)
    if milis[0] > 1500:
        milis[0] = 1500

    milis[1] = 1100+fabs(angles[1]*11)-15*11-57

    for i in range(2):
        if milis[i] < 1000:
            milis[i] = 1000

    milis[2] = 2000 - fabs(angles[2] * 11)
    if milis[2] < 1000:
        milis[2] = milis[2]+9000
    print(milis)
    send_to_stm(milis)


def main():
    angle_base = 60
    end_effector = 0
    mx = 300
    my = 100  # mouse coordinate x, y
    r = [mx, my]
    pygame.init()
    display = (WIDTH, HEIGHT)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    # angle 45, aspect ratio = x/y, the last ones are clipping plain
    # which tells when object appears and disappears in terms
    # of distance
    gluPerspective(60, (display[0]/display[1]), 0.1, 5000.)
    glTranslatef(0., 0., -1500)
    glRotatef(90, 0, 0, -1)
    glRotatef(90, 0, -1, 0)
    ground()
    arms(r)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                # moving the object
                if event.key == pygame.K_LEFT:
                    glTranslate(100, 0, 0)
                if event.key == pygame.K_RIGHT:
                    glTranslate(-100, 0, 0)
                if event.key == pygame.K_UP:
                    glTranslate(0, 0, -100)
                if event.key == pygame.K_DOWN:
                    glTranslate(0, 0, 100)
                # rotation of object
                if event.key == pygame.K_KP8:
                    glRotatef(5, 100, 0, 0)
                if event.key == pygame.K_KP2:
                    glRotatef(5, -100, 0, 0)
                if event.key == pygame.K_KP4:
                    glRotatef(5, 0, 0, 100)
                if event.key == pygame.K_KP6:
                    glRotatef(5, 0, 0, -100)
                # it's a quick patch to make base moving Z is moving base in one side, X in another
                if event.key == pygame.K_z:
                    angle_base -= 5
                    uart.send_data(angle_base)
                if event.key == pygame.K_x:
                    angle_base += 5
                    uart.send_data(angle_base)
                # +/- on keypad 
                if event.key == pygame.K_KP_PLUS:
                    end_effector = 180  # angle must be calibrated
                    uart.send_data(end_effector)
                if event.key == pygame.K_KP_MINUS:
                    end_effector = 0  # angle must be calibrated
                    uart.send_data(end_effector)
                # here it ends
                    '''
                if event.key == pygame.K_KP7:
                    t = Perpendicular()
                    glTranslatef(t[0],t[1],t[2])
                    '''
            if event.type == pygame.MOUSEBUTTONDOWN:
                r = set_mouse_input(r[0], r[1])
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        ground()
        arms(r)
        milisec(r)
        pygame.display.flip()  # updating the whole screen
        pygame.time.wait(100)
            

main()
