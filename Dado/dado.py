from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import png


window = 0

# Variables Rotation
currentRotationX = currentRotationY = currentRotationZ = 0.0


def LoadTextures():
    global texture
    texture = glGenTextures(2)

    reader = png.Reader(filename='dado.png')
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
    global currentRotationX, currentRotationY, currentRotationZ, texture

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    
    glLoadIdentity()                   
    glClearColor(0.5,0.5,0.5,1.0)            
    glTranslatef(0.0,0.0,-5.0)
    glRotatef(currentRotationX,1.0,0.0,0.0)
    glRotatef(currentRotationY,0.0,1.0,0.0)
    glRotatef(currentRotationZ,0.0,0.0,1.0)         
    

    glBindTexture(GL_TEXTURE_2D, texture[1])
    glBegin(GL_QUADS)

    # Front Face
    glTexCoord2f(0.0, 1/2); glVertex3f(-1.0, -1.0,  1.0)
    glTexCoord2f(1/3, 1/2); glVertex3f( 1.0, -1.0,  1.0)   
    glTexCoord2f(1/3, 1.0); glVertex3f( 1.0,  1.0,  1.0)   
    glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0,  1.0)  
      
    # Back Face
    glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0, -1.0)    
    glTexCoord2f(1/3, 0.0); glVertex3f(-1.0,  1.0, -1.0)    
    glTexCoord2f(1/3, 1/2); glVertex3f( 1.0,  1.0, -1.0)    
    glTexCoord2f(0.0, 1/2); glVertex3f( 1.0, -1.0, -1.0)   
    
    # Top Face
    glTexCoord2f(1/3, 1/2); glVertex3f(-1.0,  1.0, -1.0)   
    glTexCoord2f(2/3, 1/2); glVertex3f(-1.0,  1.0,  1.0)    
    glTexCoord2f(2/3, 1.0); glVertex3f( 1.0,  1.0,  1.0)    
    glTexCoord2f(1/3, 1.0); glVertex3f( 1.0,  1.0, -1.0)   

    # Bottom Face       
    glTexCoord2f(1/3, 0.0); glVertex3f(-1.0, -1.0, -1.0)   
    glTexCoord2f(2/3, 0.0); glVertex3f( 1.0, -1.0, -1.0)   
    glTexCoord2f(2/3, 1/2); glVertex3f( 1.0, -1.0,  1.0)   
    glTexCoord2f(1/3, 1/2); glVertex3f(-1.0, -1.0,  1.0)    
    
    # Right face
    glTexCoord2f(2/3, 1/2); glVertex3f( 1.0, -1.0, -1.0)    
    glTexCoord2f(1.0, 1/2); glVertex3f( 1.0,  1.0, -1.0)   
    glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0,  1.0)    
    glTexCoord2f(2/3, 1.0); glVertex3f( 1.0, -1.0,  1.0)  
    
    # Left Face
    glTexCoord2f(2/3, 0.0); glVertex3f(-1.0, -1.0, -1.0)  
    glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0,  1.0)    
    glTexCoord2f(2/3, 1/2); glVertex3f(-1.0,  1.0,  1.0)   
    glTexCoord2f(1.0, 1/2); glVertex3f(-1.0,  1.0, -1.0)   
    
    glEnd()
    
    currentRotationX = currentRotationX + 0.3
    currentRotationY = currentRotationY + 0.3
    currentRotationZ = currentRotationZ + 0.3

    glutSwapBuffers()


def main():
    global window
    glutInit(sys.argv)

    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    
    window = glutCreateWindow("Dado")

    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)

    InitGL(640, 480)

    glutMainLoop()

if __name__ == "__main__":
    main()
