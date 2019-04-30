import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from math_ik import math
from file1 import file1
from pygame.math import *
from math import fabs
import uart

WIDTH = 800
HEIGHT = 600

#angle_error is used as global variable to impose restraints on 
#range of motion of robotic arm, which results from excessively high
#torque and weak servo motors
angle_error = 0

fi1 = 60
fi2 = 30

#defines vertices of ground in coordinate system: (z,x,y) [a bit way-out]
#it's tuple not list! it's immutable
ground_vertices = (
    (1000,1000,0),
    (1000,-1000,0),
    (-1000,-1000,0),
    (-1000,1000,0)
    )

#it will be fed in Values() function by txt file
arm_vertices = []

def Ground():
    glBegin(GL_QUADS)
    for vertex in ground_vertices:
        glColor3fv((0.58,0.47,0.36))
        glVertex3fv(vertex)
    glEnd()
    glBegin(GL_LINES)
    for vertex in ground_vertices:
        glColor3fv((0.1,0.87,0.36))
        glVertex3fv(vertex)
    glEnd()

def Arms(fi1, fi2):
    Values(fi1, fi2)
    glBegin(GL_LINE_STRIP)
    glColor3fv((0.37,0.62,0.69))
    for i in range(4):
        glVertex3f(arm_vertices[3*i],arm_vertices[3*i+1],arm_vertices[3*i+2])
    glEnd()

def Values(fi1, fi2):
    measure = file1().read_file_arm()
    coordinates = math().position(fi1, fi2, measure)
    #cunning use of iteration, doesn't work if is made forward, 
    #adding zeros as z coordinate
    for i in reversed(range(4)):
        coordinates.insert(i*2, 0)
    for x in range(len(coordinates)):
        arm_vertices.insert(x, coordinates[x])


def Send_to_STM(milis, end_effector, angle_base, grip):
    dane = [str(int(angle_base)), '1500', str(int(milis[1])),
            str(int(milis[2])), str(int(end_effector)), str(int(grip))]
    #dane = ['1500', '2000', '2000', '1590', '1500', '1500']
    for i in range(6):
        uart.send_data(dane[i])


def milisec(end_effector, angle_base, grip):
    global fi1, fi2
    milis=[1500, 1500, 1500]
    measure = file1().read_file_arm()
    angles = math().position_angles(fi1, fi2, measure)
    global angle_error
    #these angles must be checked, if is made because of phisical restraints
    if angles[1] > 20 and angles[1] < 110:
        angle_error = 0 #screen will be updated
        # print(angles)
        #1st -11ms
        milis[0]=1100+fabs(angles[0]*9)
        if milis[0]>1500:
            milis[0]=1500

        milis[1]=1100+fabs(angles[1]*11)-15*11-57

        for i in range(2):
            if milis[i]<1000:
                milis[i]=1000

        milis[2] = 2000 - fabs(angles[2] * 11)
        print(angles[2], milis[2])
        if milis[2]<1000:
            milis[2]=milis[2]+9000
        # print(milis)
        Send_to_STM(milis, end_effector, angle_base, grip)
    else:
        print("Ruch niedozwolony!")
        angle_error = 1 #screen won't be updated


def main():
    global angle_error, fi1, fi2
    angle_base = 1500
    grip = 1500
    end_effector = 1500
    fi1 = 63
    fi2 = 50
    pygame.init()
    display = (WIDTH, HEIGHT)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    #angle 45, aspect ratio = x/y, the last ones are clipping plain
    #which tells when object appears and disappears in terms 
    #of distance
    gluPerspective(60, (display[0]/display[1]), 0.1, 5000.)
    glTranslatef(0., 0., -1500)
    glRotatef(90, 0, 0, -1)
    glRotatef(90, 0, -1, 0)
    Ground()
    Arms(fi1, fi2)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                #it's a quick patch to make base moving Z is moving base in one side, X in another
                if event.key == pygame.K_z and angle_base > 1000:
                    angle_base -= 50
                if event.key == pygame.K_x and angle_base < 2000:
                    angle_base += 50
                if event.key == pygame.K_m:
                    grip = 1200  # angle must be calibrated
                if event.key == pygame.K_n:
                    grip = 2200  # angle must be calibrated
                if event.key == pygame.K_o and end_effector < 2500:
                    end_effector += 50 #angle must be calibrated
                if event.key == pygame.K_p and end_effector > 1000:
                    end_effector -= 50 #angle must be calibrated
                #here it ends
                if event.key == pygame.K_k:
                    fi2 += 2
                if event.key == pygame.K_l:
                    fi2 -= 2
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Ground()
        #math error handling
        try:
            Arms(fi1, fi2)
        except ValueError as error:
            print("You've clicked too far")
            continue
        milisec(end_effector, angle_base, grip)
        #if doesn't allow to update screen if angles are inappropriate
        if angle_error == 0:
            pygame.display.flip()#updating the whole screen
        pygame.time.wait(100)


main()
