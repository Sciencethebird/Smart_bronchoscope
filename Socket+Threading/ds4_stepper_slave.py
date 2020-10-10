import RPi.GPIO as gp
import time
import socket
from threading import Thread
gp.setmode(gp.BCM)

gp.setup(18, gp.OUT)
gp.setup(23, gp.OUT)

gp.setup(4, gp.OUT)
gp.setup(24, gp.OUT)

gp.output(23, gp.HIGH)
gp.output(24, gp.HIGH)


HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

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

motor1 = run_motor(23, 18, 'cw', 0.005)
motor_thread = Thread(target = motor1.run)
motor2 = run_motor(24, 4, 'cw', 0.005)
motor_thread2 = Thread(target = motor2.run)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    strt_state = False
    strt_state2 = False
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            print(data)
            if(data == b'm1cw'):
                print('m1cw')
                if strt_state == False or motor1.speed() != 0.005:
                    motor1.terminate()
                    motor1 = run_motor(23, 18, 'cw', 0.005)
                    motor_thread = Thread(target = motor1.run)
                    motor_thread.start()
                    strt_state = True
            if(data == b'm1cwf'):
                if strt_state == False or motor1.speed() != 0.001:
                    motor1.terminate()
                    motor1 = run_motor(23, 18, 'cw', 0.001)
                    motor_thread = Thread(target = motor1.run)
                    motor_thread.start()
                    strt_state = True
            if(data == b'none'):
                print('none')
                motor1.terminate()
                strt_state = False
            if(data == b'm1ccw'):
                if strt_state == False or motor1.speed() != 0.005:
                    motor1.terminate()
                    motor1 = run_motor(23, 18, 'ccw', 0.005)
                    motor_thread = Thread(target = motor1.run)
                    motor_thread.start()
                    strt_state = True
            if(data == b'm1ccwf'):
                if strt_state == False or motor1.speed() != 0.001:
                    motor1.terminate()
                    motor1 = run_motor(23, 18, 'ccw', 0.001)
                    motor_thread = Thread(target = motor1.run)
                    motor_thread.start()
                    strt_state = True


            if(data == b'm2cw'):
                print('m2cw')
                if strt_state2 == False or motor2.speed() != 0.005:
                    motor2.terminate()
                    motor2 = run_motor(24, 4, 'cw', 0.005)
                    motor_thread2 = Thread(target = motor2.run)
                    motor_thread2.start()
                    strt_state2 = True
            if(data == b'm2cwf'):
                if strt_state2 == False or motor2.speed() != 0.001:
                    motor2.terminate()
                    motor2 = run_motor(24, 4, 'cw', 0.001)
                    motor_thread2 = Thread(target = motor2.run)
                    motor_thread2.start()
                    strt_state2 = True
            if(data == b'none2'):
                print('none2')
                motor2.terminate()
                strt_state2 = False
            if(data == b'm2ccw'):
                if strt_state2 == False or motor2.speed() != 0.005:
                    motor2.terminate()
                    motor2 = run_motor(24, 4, 'ccw', 0.005)
                    motor_thread2 = Thread(target = motor2.run)
                    motor_thread2.start()
                    strt_state2 = True
            if(data == b'm2ccwf'):
                if strt_state2 == False or motor2.speed() != 0.001:
                    motor2.terminate()
                    motor2 = run_motor(24, 4, 'ccw', 0.001)
                    motor_thread2 = Thread(target = motor2.run)
                    motor_thread2.start()
                    strt_state2 = True 
            if not data:
                break
            conn.sendall(data)



   
    

