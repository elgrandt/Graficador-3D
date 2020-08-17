__author__ = 'Dylan'
from OpenGL.GL import *
import math
import pygame

class Texture:
    def __init__(self):
        texture = 0
        width = 1
        height = 1

class Graphics:
    def __init__(self):
        pass
    def DrawEllipsoid(self, uiStacks, uiSlices, fA, fB, fC, filled = True):
        Pi = 3.1416
        tStep = Pi / uiSlices
        sStep = Pi / uiStacks
        second_parameter = GL_FILL
        if not filled:
            second_parameter = GL_LINE
        glPolygonMode(GL_FRONT_AND_BACK, second_parameter)
        t = -Pi/2
        while (t <= (Pi/2)+.0001):
            glBegin(GL_TRIANGLE_STRIP)
            s = -Pi
            while (s <= Pi+.0001):
                glVertex3f(fA * math.cos(t) * math.cos(s), fB * math.cos(t) * math.sin(s), fC * math.sin(t))
                glVertex3f(fA * math.cos(t+tStep) * math.cos(s), fB * math.cos(t+tStep) * math.sin(s), fC * math.sin(t+tStep))
                s += sStep
            glEnd()
            t += tStep
    def Cube(self, vertices, color):
        edges = (
            (0,1),
            (0,3),
            (0,4),
            (2,1),
            (2,3),
            (2,7),
            (6,3),
            (6,4),
            (6,7),
            (5,1),
            (5,4),
            (5,7)
        )

        surfaces = (
            (0,1,2,3),
            (3,2,7,6),
            (6,7,5,4),
            (4,5,1,0),
            (1,5,7,2),
            (4,0,3,6)
        )

        glBegin(GL_QUADS)

        for surface in surfaces:
            x = 0
            glColor3fv(color)
            for vertex in surface:
                x+=1
                glVertex3fv(vertices[vertex])

        glEnd()

        glBegin(GL_LINES)
        for edge in edges:
            for vertex in edge:
                glVertex3fv(vertices[vertex])
        glEnd()
    def GenerateTexture(self,surface):
        textureData = pygame.image.tostring(surface, "RGBA", 1)
        width = surface.get_width()
        height = surface.get_height()

        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

        ret = Texture()
        ret.width = width
        ret.height = height
        ret.texture = texture
        return ret
    def BlitTexture(self, texture, w, h, x, y, rx = 1, ry = 1):
        glBindTexture( GL_TEXTURE_2D, texture )
        glEnable( GL_TEXTURE_2D )

        glBegin(GL_QUADS)
        glTexCoord2f(   0,   0 );  glVertex2f(x    ,  y )
        glTexCoord2f(rx  ,   0 );  glVertex2f(x + w,  y )
        glTexCoord2f(rx  ,  -ry);  glVertex2f(x + w,  y + h)
        glTexCoord2f(0   ,  -ry);  glVertex2f(x    ,  y + h)
        glEnd()

        glDisable( GL_TEXTURE_2D )

OGL = Graphics()