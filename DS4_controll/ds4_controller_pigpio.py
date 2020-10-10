import pygame
import RPi.GPIO as gp
import time
import socket
import pigpio

# connect to local Pi


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
        
#class motor_wave_generator:
        
class decoder:

   """Class to decode mechanical rotary encoder pulses."""

   def __init__(self, pi, gpioA, gpioB, callback):


      self.pi = pi
      self.gpioA = gpioA
      self.gpioB = gpioB
      self.callback = callback

      self.levA = 0
      self.levB = 0

      self.lastGpio = None

      self.pi.set_mode(gpioA, pigpio.INPUT)
      self.pi.set_mode(gpioB, pigpio.INPUT)

      self.pi.set_pull_up_down(gpioA, pigpio.PUD_UP)
      self.pi.set_pull_up_down(gpioB, pigpio.PUD_UP)

      self.cbA = self.pi.callback(gpioA, pigpio.EITHER_EDGE, self._pulse)
      self.cbB = self.pi.callback(gpioB, pigpio.EITHER_EDGE, self._pulse)

   def _pulse(self, gpio, level, tick):


      if gpio == self.gpioA:
         self.levA = level
      else:
         self.levB = level;

      if gpio != self.lastGpio: # debounce
         self.lastGpio = gpio

         if   gpio == self.gpioA and level == 1:
            if self.levB == 1:
               self.callback(1)
         elif gpio == self.gpioB and level == 1:
            if self.levA == 1:
               self.callback(-1)

   def cancel(self):


      self.cbA.cancel()
      self.cbB.cancel()
    
class motor:
    def __init__(self, clk_pin, dir_pin):
        self.pi = pigpio.pi()
        
        self._running = False
        self._clkpin = clk_pin
        self._dirpin = dir_pin
        
        self.pi.set_mode(self._clkpin, pigpio.OUTPUT)
        self.pi.set_mode(self._dirpin, pigpio.OUTPUT)
        
        self._time = 100
        self._dir = 'cw'

        self._pos = 0
        self._returning = False
    def encoder_callback(self, way):
        self._pos += way
        print("pos={}".format(self._pos))
      
    def set_encoder(self, pin1, pin2):
        self._decoder = decoder(self.pi, pin1, pin2, self.encoder_callback)
        
    def run(self, dt, direction):
        
        if self._dir != direction:
            self._dir = direction
            if direction == 'cw':
                self.pi.write(self._dirpin, 0)
            if direction == 'ccw':
                self.pi.write(self._dirpin, 1)
        if self._running == False or self._time != dt:
            self._running = True
            self._time = dt
            
            square = []
            square.append(pigpio.pulse(1<<self._clkpin, 0,       self._time))
            square.append(pigpio.pulse(0,       1<<self._clkpin, self._time))
            
            #self.pi.wave_clear()
            self.pi.wave_add_generic(square)
            self._wid = self.pi.wave_create()
            if self._wid >= 0:
               self.pi.wave_send_repeat(self._wid)
                 
    def stop(self):
        
        if self._running == True and self._returning == False:
            print('stop')
            self._running = False
            self.pi.wave_tx_stop()
            try:
                print('s')
                #self.pi.wave_delete(self._wid)
                #self.pi.wave_clear()
            except:
                print('lol')
    def move_to_origin(self):
        print('gggggggggggg')
        self._returning = True 
    def check_returned(self):
        #self.run(self._time, self._dir)
        if self._returning == True:
            if self._pos >1:
                self.run(500, 'cw')
            if self._pos <-1:
                self.run(500, 'ccw') 
            if self._pos<=1 and self._pos>=-1:
                print('yoyo', self._pos)
                self._returning = False
                self.stop()
            
            
    def __del__(self):
       # self.pi.wave_tx_stop()
        #self.pi.wave_delete(self._wid)
        #self.pi.wave_clear()
        self._decoder.cancel()

m1 = motor(23, 4)
m2 = motor(24, 18)
m1.set_encoder(20, 21)
m2.set_encoder(26, 19)
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

    m1.check_returned()
    m2.check_returned()
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
            if i == 0: # left stick horizontal
                
                if axis > 0.3 and axis < 0.8:
                    m1.run(1000, 'cw')
                if axis > 0.8:
                    m1.run(500, 'cw')
                if axis<0.2 and axis> -0.2:
                    m1.stop()
                if axis <-0.3 and axis > -0.8:
                    m1.run(1000, 'ccw')
                if axis <-0.8:
                    m1.run(500, 'ccw')

            if i == 1: # left stick vertical
                
                if axis > 0.3 and axis < 0.8:
                    m2.run(1000, 'cw')
                if axis > 0.8:
                    m2.run(500, 'cw')
                if axis<0.2 and axis> -0.2:
                    m2.stop()
                if axis <-0.3 and axis > -0.8:
                    m2.run(1000, 'ccw')
                if axis <-0.8:
                    m2.run(500, 'ccw')
                
        textPrint.unindent()
            
        buttons = joystick.get_numbuttons()
        textPrint.print(screen, "Number of buttons: {}".format(buttons) )
        textPrint.indent()

        for i in range( buttons ):
            button = joystick.get_button( i )
            if i == 0 and button == 1:
                m1.move_to_origin()
            if i == 1 and button == 1:
                m2.move_to_origin()
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
