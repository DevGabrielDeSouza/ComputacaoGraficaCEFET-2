from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import png
import math

window = 0

n1 = 50
n2 = 50
r = 1.8

a = 0

# Variables Rotation 
currentRotationX = 180.0
currentRotationY = currentRotationZ = 0.0
offsetRotationX = 0
offsetRotationY = 0.6
offsetRotationZ = 0

def f1(i,j,theta,phi):
    
    x = r*math.cos(theta)*math.cos(phi)
    y = r*math.sin(theta)
    z = r*math.cos(theta)*math.sin(phi)
    return x,y,z

def s(theta):
    return theta/(2*math.pi)
def t(phi):
    return ((phi/math.pi)+(1/2))

def LoadTextures():
    global texture
    texture = glGenTextures(2)

    reader = png.Reader(filename='mapa.png')
    w, h, pixels, metadata = reader.read_flat()
    if(metadata['alpha']):
        modo = GL_RGBA
    else:
        modo = GL_RGB
    glBindTexture(GL_TEXTURE_2D, texture[0])
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
    global currentRotationX, currentRotationY, currentRotationZ, texture

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    
    glLoadIdentity()                   
    glClearColor(0.5,0.5,0.5,1.0)            
    glTranslatef(0.0,0.0,-5.0)
    glRotatef(currentRotationX,1.0,0.0,0.0)          
    glRotatef(currentRotationY,0.0,1.0,0.0)           
    glRotatef(currentRotationZ,0.0,0.0,1.0) 

    glBindTexture(GL_TEXTURE_2D, texture[0])              
    for i in range(0,n1): 
        glBegin(GL_QUAD_STRIP)
        for j in range(0,n2): 
            theta = (math.pi*i/(n1-1))-(math.pi/2)
            phi = 2*math.pi*j/(n2-1)
            x,y,z = f1(i,j,theta,phi)
            glTexCoord2f(s(phi), t(theta)); glVertex3f(x,y,z)
            theta = (math.pi*(i+1)/(n1-1))-(math.pi/2)
            x,y,z = f1(i+1,j,theta,phi)
            glTexCoord2f(s(phi), t(theta)); glVertex3f(x,y,z)
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
    
    window = glutCreateWindow("Globo com a textura do mapa mundi")

    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    
    InitGL(640, 480)
    glutMainLoop()

if __name__ == "__main__":
    main()
