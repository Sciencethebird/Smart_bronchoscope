import serial

port = '/dev/ttyACM0'

s1 = serial.Serial(port, 9600)
s = [0]
while True:
    rs = s1.readline()
    
    
    print(rs)
