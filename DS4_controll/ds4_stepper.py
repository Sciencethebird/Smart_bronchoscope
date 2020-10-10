import RPi.GPIO as gp
import time
import socket
from threading import Thread
import serial





gp.setmode(gp.BCM)

gp.setup(18, gp.OUT)
gp.setup(23, gp.OUT)

gp.setup(4, gp.OUT)
gp.setup(24, gp.OUT)

gp.output(23, gp.HIGH)
gp.output(24, gp.HIGH)


HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

class encoder_class:
    def __init__(self, pin1, pin2, name = None):
        self._pin1 = pin1
        self._pin2 = pin2
        self._degree = 0
        self._running = True
        self._name = name
        gp.setup(self._pin1, gp.IN, pull_up_down=gp.PUD_UP)
        gp.setup(self._pin2, gp.IN, pull_up_down=gp.PUD_UP)
    
    def run(self):
        while self._running:
            print(self._name, self._degree)
            p1a = gp.input(self._pin1)
            p2a = gp.input(self._pin2)
            
            while p1a == 0 and p2a == 0:
                #print(1)
                p1b = gp.input(self._pin1)
                p2b = gp.input(self._pin2)
                if p1b == 1 and p2b == 0:
                    self._degree +=1
                    break
                if p1b == 0 and p2b == 1:
                    self._degree -=1
                    break
            while p1a == 0 and p2a == 1:
                #print(2)
                p1b = gp.input(self._pin1)
                p2b = gp.input(self._pin2)
                if p1b == 0 and p2b == 0:
                    self._degree +=1
                    break
                if p1b == 1 and p2b == 1:
                    self._degree -=1
                    break
            while p1a == 1 and p2a == 0:
                #print(3)
                p1b = gp.input(self._pin1)
                p2b = gp.input(self._pin2)
                if p1b == 1 and p2b == 1:
                    self._degree +=1
                    break
                if p1b == 0 and p2b == 0:
                    self._degree -=1
                    break
            while p1a == 1 and p2a == 1:
                #print(4)
                p1b = gp.input(self._pin1)
                p2b = gp.input(self._pin2)
                if p1b == 0 and p2b == 1:
                    self._degree +=1
                    break
                if p1b == 1 and p2b == 0:
                    self._degree -=1
                    break
    def degree(self):
        return self._degree
    def terminate(self):
        self._running = False

class run_motor:
    def __init__(self, motor_clk_pin, motor_dir_pin, direction, speed):
        self._running = True
        self._clk_pin = motor_clk_pin
        self._dir_pin = motor_dir_pin
        self._speed = speed
       
        if direction == 'cw':
            self._dir = gp.LOW 
        if direction == 'ccw':
            self._dir = gp.HIGH
    def terminate(self):
        self._running = False
    def speed(self):
        return self._speed
    def run(self):
        gp.output(self._dir_pin, self._dir)
        while self._running:
            gp.output(self._clk_pin, gp.LOW)
            time.sleep(self._speed) #0.005
            gp.output(self._clk_pin, gp.HIGH)
            time.sleep(self._speed)

class motor:
    def __init__(self, clk_pin, dir_pin, en_pin1, en_pin2, encoder_name = None):
        self._clk_pin = clk_pin
        self._dir_pin = dir_pin
        
        self._dir = 'cw'
        self._dt = 0.005
        self._degree = int(0)
        
        self._motorstate = False
        
        self._motor = run_motor(self._clk_pin, self._dir_pin, 'cw', 0.005)
        self._thread = Thread(target = self._motor.run)
        self._returning = False 
        self._encoder_enabled = False
        
        if encoder_name != None:
            self._encoder_enabled = True
            self._encoder = encoder_class(en_pin1, en_pin2, encoder_name)
            self._encoder_thread = Thread(target = self._encoder.run)
            self._encoder_thread.start()
        
    def run(self, DIR, dt):
        
        if self._motorstate == False or self._dt != dt or self._dir != DIR:
            self._motor.terminate()
            
            self._dir = DIR
            self._dt = dt
            self._motorstate = True
            
            self._motor = run_motor(self._clk_pin, self._dir_pin, self._dir, self._dt)
            self._thread = Thread(target = self._motor.run)
            self._thread.start()
            
        
    def stop(self):
        if not self._returning:
            print('stop')
            self._motor.terminate()
            self._motorstate = False
        
    def update_degree(self):     
        if self._encoder_enabled:
            self._degree =self._encoder.degree()
            print(self._degree)
            if self._degree <5 and self._degree > -5:
                if self._returning == True:
                    self._returning = False
                    self.stop() 
               
                
    def move_to_origin(self):
        self._returning = True
        if self._degree >0:
            self.run('ccw', 0.001)
                
        elif self._degree <0:
            self.run('cw', 0.001)
        
        

m1 = motor(23, 18, 20, 21)
m2 = motor(24, 4, 19, 26)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        #print('Connected by', addr)
        while True:
            
            data = conn.recv(1024)
            #print(data)
            m1.update_degree()
            if(data == b'm1zero'):
                m1.move_to_origin()
            if(data == b'm1cw'):
                m1.run('cw', 0.0005)
            if(data == b'm1cwf'):
                m1.run('cw', 0.0001)
            if(data == b'none'):
                m1.stop()
            if(data == b'm1ccw'):
                m1.run('ccw', 0.0005)
            if(data == b'm1ccwf'):
                m1.run('ccw', 0.0001)
            if(data == b'm2cw'):
                m2.run('cw', 0.0005)
            if(data == b'm2cwf'):
                m2.run('cw', 0.0001)
            if(data == b'none2'):
                m2.stop()
            if(data == b'm2ccw'):
                m2.run('ccw', 0.0005)
            if(data == b'm2ccwf'):
                m2.run('ccw', 0.0001)

            
            if not data:
                break
            conn.sendall(data)

encoder.terminate()

   
    

