import RPi.GPIO as gp
import time
import socket
from threading import Thread
import serial

gp.setmode(gp.BCM)

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
                
encoder = encoder_class(20, 21, 'm1')
t = Thread(target = encoder.run)
t.start()

encoder1 = encoder_class(19, 26, 'm2')
t1 = Thread(target = encoder1.run)
t1.start()
    

