from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import png

from math import *
import math
import random

dist = 2

side_count = 6

window = 0
	
height = 1.8

side_rads_size = (2*math.pi)/side_count

down_radius = 1.3
up_radius = 0.5
down_vertices = []
up_vertices = []



currentRotationX = currentRotationY = currentRotationZ = 0.0
offsetRotationX = 0.6
offsetRotationY = 0.2
offsetRotationZ = 0.4

def LoadTextures():
	global texture
	texture = glGenTextures(2) 

	reader = png.Reader(filename='textura.png')
	w, h, pixels, metadata = reader.read_flat()
	if(metadata['alpha']):
		modo = GL_RGBA
	else:
		modo = GL_RGB
	glBindTexture(GL_TEXTURE_2D, texture[1])
	glPixelStorei(GL_UNPACK_ALIGNMENT,1)
	glTexImage2D(GL_TEXTURE_2D, 0, modo, w, h, 0, modo, GL_UNSIGNED_BYTE, pixels.tolist())
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
	glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

def InitGL(Width, Height):             
	LoadTextures()
	glEnable(GL_TEXTURE_2D)
	glClearColor(0.0, 0.0, 0.0, 0.0) 
	glClearDepth(1.0)
	glDepthFunc(GL_LESS)               
	glEnable(GL_DEPTH_TEST)            
	glShadeModel(GL_SMOOTH)            
	glMatrixMode(GL_PROJECTION)
	gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
	glMatrixMode(GL_MODELVIEW)

def ReSizeGLScene(Width, Height):
	if Height == 0:                        
		Height = 1
	glViewport(0, 0, Width, Height)      
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
	glMatrixMode(GL_MODELVIEW)

def DrawGLScene():
	global currentRotationX, currentRotationY, currentRotationZ, texture, down_vertices, up_vertices

	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    
	glLoadIdentity()                   
	glClearColor(0.5,0.5,0.5,1.0)            
	glTranslatef(0.0,0.0,-5.0)
	glRotatef(currentRotationX,1.0,0.0,0.0)
	glRotatef(currentRotationY,0.0,1.0,0.0)
	glRotatef(currentRotationZ,0.0,0.0,1.0)

	glBindTexture(GL_TEXTURE_2D, texture[1])
	glBegin(GL_POLYGON)

	# Creating and drawing down vertices
	for i in range(0,side_count):
		x = down_radius * math.cos(i*side_rads_size)
		y = down_radius * math.sin(i*side_rads_size)
		glTexCoord2f(math.cos(i), math.sin(i))
		down_vertices += [ (x,y) ]
		glVertex3f(x,y,0.0)
	glEnd()

	# Creating and drawing up vertices
	glBegin(GL_POLYGON)
	for i in range(0,side_count):
		x = up_radius * math.cos(i*side_rads_size)
		y = up_radius * math.sin(i*side_rads_size)
		glTexCoord2f(math.cos(i), math.sin(i))
		up_vertices += [ (x,y) ]
		glVertex3f(x,y,height)
	glEnd()

	#Drawing side faces
	glBegin(GL_QUADS)
	for i in range(0,side_count):
		glTexCoord2f(0.0, 1.0); glVertex3f(down_vertices[i][0],down_vertices[i][1],0.0)
		glTexCoord2f(0.0, 0.0); glVertex3f(up_vertices[i][0],up_vertices[i][1],height)
		glTexCoord2f(1.0, 0.0); glVertex3f(up_vertices[(i+1)%side_count][0],up_vertices[(i+1)%side_count][1],height)
		glTexCoord2f(1.0, 1.0); glVertex3f(down_vertices[(i+1)%side_count][0],down_vertices[(i+1)%side_count][1],0.0)
	glEnd()
    
	currentRotationX = currentRotationX + offsetRotationX
	currentRotationY = currentRotationY + offsetRotationY
	currentRotationZ = currentRotationZ + offsetRotationZ

	glutSwapBuffers()


def main():
	global window
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
	glutInitWindowSize(640, 480)
	glutInitWindowPosition(0, 0)
	
	window = glutCreateWindow("Tronco de Pirâmide com a textura de pedras")

	glutDisplayFunc(DrawGLScene)
	glutIdleFunc(DrawGLScene)
	glutReshapeFunc(ReSizeGLScene)
	
	InitGL(640, 480)

	glutMainLoop()

if __name__ == "__main__":
	main()