import pygame
import RPi.GPIO as gp
import time
import socket
import serial

gp.setmode(gp.BCM)

gp.setup(18, gp.OUT)#interrupt

HOST = '127.0.0.1'
PORT = 65432
ser = serial.Serial(port = '/dev/ttyACM0',baudrate = 9600, timeout = 0.5)

#ser = serial.Serial(port = '/dev/ttyUSB0',baudrate = 9600, timeout = 0.5)
#ser = serial.Serial(port = '/dev/serial0',baudrate = 9600)

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def print(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height
        
    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15
        
    def indent(self):
        self.x += 10
        
    def unindent(self):
        self.x -= 10
class motors_message:
    def __init__(self):
        self._message_A = 'm1stop'
        self._message_B = 'm2stop'
    def run(self, message):
        print( message, self._message_A, self._message_B)
        if message != self._message_A and message != self._message_B:
            #ser = serial.Serial(port = '/dev/ttyACM0',baudrate = 9600, timeout = 0.5)
            if message[1] == '1':
                self._message_A = message
            if message[1] == '2':
                self._message_B = message 
            message = self._message_A + self._message_B+ '\r\n'
            print(message)
            gp.output(18, gp.HIGH)
            time.sleep(0.001)
            ser.write(message.encode() )
            ser.flush()
            gp.output(18, gp.LOW)
            #ser.close()
class motor:
    def __init__(self, message_handler = None):
        self.message = 'none'
    
    def run(self, message):
        #print(message , self.message)
        if message != self.message:
            
            print(message)
            #global ser
            gp.output(18, gp.HIGH)
            self.message = message
          
            message += '\r\n'
            ser.write(message.encode() )
            gp.output(18, gp.LOW)
            ser.close()
          
            

#m1 = motor()
#m2 = motor('none2')
m = motors_message()
        
pygame.init()
 
# Set the width and height of the screen [width,height]
size = [500, 700]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()
    
# Get ready to print
textPrint = TextPrint()

# -------- Main Program Loop -----------
while done==False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
        
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")
            
 
    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    textPrint.reset()

    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()

    textPrint.print(screen, "Number of joysticks: {}".format(joystick_count) )
    textPrint.indent()
    
    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
    
        textPrint.print(screen, "Joystick {}".format(i) )
        textPrint.indent()
    
        # Get the name from the OS for the controller/joystick
        name = joystick.get_name()
        textPrint.print(screen, "Joystick name: {}".format(name) )
        
        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()
        textPrint.print(screen, "Number of axes: {}".format(axes) )
        textPrint.indent()
       
        #print(ser.readline())
        
        for i in range( axes ):
            axis = joystick.get_axis( i )
            textPrint.print(screen, "Axis {} value: {:>6.3f}".format(i, axis) )
            #print('sss')
            if i == 0: # left stick horizontal
                
                if axis > 0.3 and axis < 0.8:
                    m.run('m1cwxx')
                    
                if axis > 0.8:
                    m.run('m1cwfx')
                if axis<0.2 and axis> -0.2:
                    m.run('m1stop')
                if axis <-0.3 and axis > -0.8:
                    m.run('m1ccwx')
                if axis <-0.8:
                    m.run('m1ccwf')
            if i == 1: # left stick vertical
                
                if axis > 0.3 and axis < 0.8:
                    m.run('m2cwxx')
                if axis > 0.8:
                    m.run('m2cwfx')
                if axis<0.2 and axis> -0.2:
                    m.run('m2stop')
                if axis <-0.3 and axis > -0.8:
                    m.run('m2ccwx')
                if axis <-0.8:
                    m.run('m2ccwf')
                   
        textPrint.unindent()
            
        buttons = joystick.get_numbuttons()
        textPrint.print(screen, "Number of buttons: {}".format(buttons) )
        textPrint.indent()

        for i in range( buttons ):
            button = joystick.get_button( i )
            if i == 0 and button == 1:
                s.sendall(b'm1zero') 
            
            textPrint.print(screen, "Button {:>2} value: {}".format(i,button) )
        textPrint.unindent()
            
        # Hat switch. All or nothing for direction, not like joysticks.
        # Value comes back in an array.
        hats = joystick.get_numhats()
        textPrint.print(screen, "Number of hats: {}".format(hats) )
        textPrint.indent()

        for i in range( hats ):
            hat = joystick.get_hat( i )
            textPrint.print(screen, "Hat {} value: {}".format(i, str(hat)) )
        textPrint.unindent()
        
        textPrint.unindent()

    
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second
    clock.tick(20)
    
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
gp.cleanup()
pygame.quit ()
