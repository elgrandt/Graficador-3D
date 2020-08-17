__author__ = 'Dylan'
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
import copy
import random
from OGL import OGL
from math import *

global rango,escala,colors
rango = 5.0
definicion = 40.0
escala = rango / definicion
colors = []

def resolver_ecuacion(ecuacion,x,y):
    # INGRESAR ECUACION MANUALMENTE (PROXIMAMENTE INTERPRETADOR AUTOMATICO DE TEXTO)
    return eval(ecuacion)

def generate_points(ecuacion):
    global rango,escala
    points = []
    maxX,maxY,maxZ = 0,0,0
    for x in range(int((rango*2)/escala)):
        points.append([])
        global colors
        colors.append([random.randrange(10)/10.0,random.randrange(10)/10.0,random.randrange(10)/10.0])
        for y in range(int((rango*2)/escala)):
            if -rango+x*escala > maxX:
                maxX = -rango+x*escala
            if -rango+y*escala > maxY:
                maxY = -rango+y*escala
            points[x].append(resolver_ecuacion(ecuacion,-rango+x*escala,-rango+y*escala))
            if points[x][y] > maxZ:
                maxZ = points[x][y]
    return points,[maxX,maxY,maxZ]

def ejes(max):
    rad = [-max[0],0.0,0.0,0.0]
    glColor3f(1.0, 0.0, 0.0);
    for position in range(3):
        rad = [0.0,0.0,0.0]
        rad[position] = -max[position]
        rad2 = copy.deepcopy(rad)
        rad2[position] = max[position]

        glLineWidth(2.0)

        glBegin(GL_LINES)

        glVertex3f(rad[0],rad[1],rad[2])
        glVertex3f(rad2[0],rad2[1],rad2[2])

        glEnd()

def graficar(points):
    # POINTS [X] [Y] = Z
    global rango,escala
    max = int((rango*2)/escala)
    for y in range(max-1,1,-1):
        global colors
        glColor3f(colors[y][0],colors[y][1],colors[y][2])

        glBegin(GL_QUAD_STRIP)

        glVertex3f(-rango+(max-1)*escala,-rango+y*escala,points[max-1][y])
        glVertex3f(-rango+(max-1)*escala,-rango+(y-1)*escala,points[max-1][y-1])
        for x in range(max-2,0,-1):
            glVertex3f(-rango+x*escala,-rango+y*escala,points[x][y])
            glVertex3f(-rango+(x)*escala,-rango+(y-1)*escala,points[x][y-1])

        glEnd()

def update3d(points,max):
    ejes(max)
    graficar(points)

def update2d():
    test_surf = pygame.Surface((800,600))
    test_surf.fill ((255,0,0))
    tex = OGL.GenerateTexture(test_surf)
    OGL.BlitTexture(tex.texture, tex.width, tex.height, 0, 0)

def manage_events():
    movement = 0.4
    x_move,y_move,anglex,angley = -1,-1,-1,-1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_move = movement
            if event.key == pygame.K_RIGHT:
                x_move = -movement

            if event.key == pygame.K_UP:
                y_move = -movement
            if event.key == pygame.K_DOWN:
                y_move = movement
            if event.key == pygame.K_a:
                anglex = movement
            if event.key == pygame.K_d:
                anglex = -movement
            if event.key == pygame.K_w:
                angley = movement
            if event.key == pygame.K_s:
                angley = -movement
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_move = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                y_move = 0
            if event.key == pygame.K_a or event.key == pygame.K_d:
                anglex = 0
            if event.key == pygame.K_w or event.key == pygame.K_s:
                angley = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                glTranslatef(0,0,1.0)
            if event.button == 5:
                glTranslatef(0,0,-1.0)
    return x_move,y_move,anglex,angley

def main():
    pygame.init()
    display_size = (800,600)
    pygame.display.set_mode(display_size, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display_size[0]/display_size[1]), 0.1, 200.0)

    glTranslatef(0,0,-50)

    x_move, y_move, z_move = 0,0,0
    anglex = 0
    angley = 0

    points, max = generate_points("x*x-y*y")
    while True:
        x_move2,y_move2,anglex2,angley2 = manage_events()
        if x_move2 != -1: x_move = x_move2
        if y_move2 != -1: y_move = y_move2
        if anglex2 != -1: anglex = anglex2
        if angley2 != -1: angley = angley2

        glClearColor(1,1,1,1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glTranslatef(x_move, y_move, z_move)
        glRotatef(anglex,0,1,0)
        glRotatef(angley,1,0,0)

        update3d(points,max)

        #update2d()

        pygame.display.flip()

        pygame.time.wait(10)

if __name__ == "__main__":
    main()