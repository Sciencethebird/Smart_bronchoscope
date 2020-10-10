import pygame
import RPi.GPIO as gp
import time
from threading import Thread
import multiprocessing as mt


gp.setmode(gp.BCM)

gp.setup(24, gp.OUT) # motor 1 cw

gp.setup(18, gp.OUT)
gp.setup(23, gp.OUT)

gp.output(23, gp.HIGH)  # motor 1 step
gp.output(18, gp.LOW)   # motor 1 dir

def stpr_rotate():
    
    for i in range(500):
        gp.output(23, gp.LOW)
        time.sleep(0.00005)
        gp.output(23, gp.HIGH)
        time.sleep(0.00005)



# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

class run_motor:
    def __init__(self):
        self._running = True
        #if direction == 'cw':
        #self._dir = gp.LOW
        #if direction == 'ccw':
        self._dir = gp.HIGH
    def terminate(self):
        self._running = False
    def run(self):
        gp.output(18, self._dir)
        while self._running:
            gp.output(23, gp.LOW)
            time.sleep(0.0005)
            gp.output(23, gp.HIGH)
            time.sleep(0.0005)
            

motor1 = run_motor()
motor_thread = mt.Process(motor1.run())
strt_state = False

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
        
        for i in range( axes ):
            axis = joystick.get_axis( i )
            textPrint.print(screen, "Axis {} value: {:>6.3f}".format(i, axis) )
            if i == 0: # left stick
                if axis > 0.5:
                    print('cw')
                    if strt_state == False:
                        #motor1 = run_motor()
                        #motor_thread = Thread(target = motor1.run())
                        motor_thread.start()
                        strt_state = True
                if axis<0.2 and axis>-0.2:
                    print('none')
                    if strt_state == True:
                        motor1.terminate()
                        strt_state = False
                        
                if axis <-0.5:
                    strt_state = True
                
                
        textPrint.unindent()
            
        buttons = joystick.get_numbuttons()
        textPrint.print(screen, "Number of buttons: {}".format(buttons) )
        textPrint.indent()

        for i in range( buttons ):
            button = joystick.get_button( i )
            if button == 1 and i == 0:
                 gp.output(24, gp.HIGH)
                 s.sendall(b'lala')
                 data = s.recv(1024)
                 print('Recerved', repr(data))
                 
            if button == 0 and i == 0:
                 gp.output(24, gp.LOW)
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
