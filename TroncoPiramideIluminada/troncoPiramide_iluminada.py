from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from math import *
import math 
import sys
import random

#Pyramid Settings
side_count = random.randrange(3, 12)
height = 4
side_rads_size = (2*math.pi)/side_count
down_radius = 1.3
up_radius = 0.5
down_vertices = []
up_vertices = []


#Variables for Rotation
currentRotationX = currentRotationY = currentRotationZ = 0.0
offsetRotationX = 0.6
offsetRotationY = 0.2
offsetRotationZ = 0.4


def draw_pyramid():
	global currentRotationX, currentRotationY, currentRotationZ, down_vertices, up_vertices

	glPushMatrix()
	
	glRotatef(currentRotationX,1.0,0.0,0.0)
	glRotatef(currentRotationY,0.0,1.0,0.0)
	glRotatef(currentRotationZ,0.0,0.0,1.0)


	# Creating and drawing down vertices
	glBegin(GL_POLYGON)
	for i in range(0,side_count):
		x = down_radius * math.cos(i*side_rads_size)
		y = down_radius * math.sin(i*side_rads_size)
		down_vertices += [ (x,y) ]

		if i == 2:
			glNormal3fv(calculaNormalFaceTri((down_vertices[0][0], down_vertices[0][1], 0.0), (down_vertices[1][0], down_vertices[1][1], 0.0), (down_vertices[2][0], down_vertices[2][1], 0.0)))
		glVertex3f(x,y,0.0)
	glEnd()



	# Creating and drawing up vertices
	glBegin(GL_POLYGON)
	for i in range(0,side_count):
		x = up_radius * math.cos(i*side_rads_size)
		y = up_radius * math.sin(i*side_rads_size)
		up_vertices += [ (x,y) ]
		if i == 2:
			glNormal3fv(calculaNormalFaceTri((up_vertices[0][0], up_vertices[0][1], height), (up_vertices[1][0], up_vertices[1][1], height), (up_vertices[2][0], up_vertices[2][1], height)))
		glVertex3f(x,y,height)
	glEnd()
	

	#Drawing side faces
	glBegin(GL_QUADS)
	for i in range(0,side_count):
		glNormal3fv(calculaNormalFaceTri( (down_vertices[i][0],down_vertices[i][1],0.0), (0,0,height), (down_vertices[(i+1)%side_count][0],down_vertices[(i+1)%side_count][1],0.0)))
		glVertex3f(down_vertices[i][0],down_vertices[i][1],0.0)
		glVertex3f(up_vertices[i][0],up_vertices[i][1],height)
		glVertex3f(up_vertices[(i+1)%side_count][0],up_vertices[(i+1)%side_count][1],height)
		glVertex3f(down_vertices[(i+1)%side_count][0],down_vertices[(i+1)%side_count][1],0.0)
	glEnd()

	currentRotationX = currentRotationX + offsetRotationX
	currentRotationY = currentRotationY + offsetRotationY
	currentRotationZ = currentRotationZ + offsetRotationX 

	glPopMatrix()


def calculaNormalFaceTri(a, b, c):
    x = 0
    y = 1
    z = 2
    v0 = a
    v1 = b
    v2 = c
    U = ( v2[x]-v0[x], v2[y]-v0[y], v2[z]-v0[z] )
    V = ( v1[x]-v0[x], v1[y]-v0[y], v1[z]-v0[z] )
    N = ( (U[y]*V[z]-U[z]*V[y]),(U[z]*V[x]-U[x]*V[z]),(U[x]*V[y]-U[y]*V[x]))
    NLength = sqrt(N[x]*N[x]+N[y]*N[y]+N[z]*N[z])
    return ( N[x]/NLength, N[y]/NLength, N[z]/NLength)

def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glRotatef(2,1,3,0)
    draw_pyramid()
    glutSwapBuffers()

def timer(i):
    glutPostRedisplay()
    glutTimerFunc(50,timer,1)

def reshape(w,h):
    glViewport(0,0,w,h)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45,float(w)/float(h),0.1,50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Virtual Camera
    gluLookAt( 10,0,0, 0,0,0,     0,1,0 )

def init():
    mat_ambient = (0.4, 0.0, 0.0, 1.0)
    mat_diffuse = (1.0, 0.0, 0.0, 1.0)
    mat_specular = (1.0, 0.5, 0.5, 1.0)
    mat_shininess = (50,)
    light_position = (5.0, 5.0, 5.0, 0.0)
    glClearColor(0.0,0.0,0.0,0.0)
    glShadeModel(GL_FLAT)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_MULTISAMPLE)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE)
    glutInitWindowSize(800,600)
    glutCreateWindow("Tronco de Pirâmide iluminado")
    glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    glutTimerFunc(50,timer,1)
    init()
    glutMainLoop()

main()
