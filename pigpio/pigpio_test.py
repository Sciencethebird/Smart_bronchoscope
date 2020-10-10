import time
import pigpio

GPIO=21
GPIO2=20
square = []
square2 = []
#                          ON       OFF    MICROS
square.append(pigpio.pulse(1<<GPIO, 0,       0))
square.append(pigpio.pulse(1<<GPIO2, 0,       500000))
square.append(pigpio.pulse(0, 0,       500000))
square.append(pigpio.pulse(0,       1<<GPIO, 0))
square.append(pigpio.pulse(0,       1<<GPIO2, 500000))
GPIOs = [21, 3, 20]
def create_wave(T_list):
    global GPIOs
    print(max(T_list) )
    period = max(T_list) 
    square = []
    lol = []
    for time_stamp in range(0,period+1,5):
        print(time_stamp)
        for idx, T in enumerate(T_list):
            if T == 0:
                square.append(pigpio.pulse(0, 1<<GPIOs[idx],0))
                continue
            if time_stamp % T == 0:
                square.append(pigpio.pulse(1<<GPIOs[idx], 0,0))
                lol.append(idx+1)
            if time_stamp % (T/2) == 0 and time_stamp % T != 0 :
                square.append(pigpio.pulse(0, 1<<GPIOs[idx],0))
                lol.append(-(idx+1))
        square.append(pigpio.pulse(0, 0,100))
        lol.append(0)
    print(lol)
    return  square
square = create_wave([1000, 0, 0])

lol = {'a':123, 'f':341, 'd':'aa'}
print(lol.values())
pi = pigpio.pi() # connect to local Pi

pi.set_mode(GPIO, pigpio.OUTPUT)
pi.set_mode(GPIO2, pigpio.OUTPUT)
#pi.set_PWM_frequency(GPIO, 2)
#pi.set_servo_pulsewidth(GPIO,1000)
#pi.set_servo_pulsewidth(GPIO2,500)
#time.sleep(2)


pi.wave_add_generic(square)
#pi.wave_add_generic(square2)
wid = pi.wave_create()

if wid >= 0:
   pi.wave_send_repeat(wid)
   time.sleep(5)
   pi.wave_tx_stop()
   pi.wave_delete(wid)

   pi.write(GPIO, 0)
   pi.write(GPIO2, 0)
   
square = create_wave([250, 500, 250])  
pi.wave_add_generic(square)
#pi.wave_add_generic(square2)
wid = pi.wave_create()

if wid >= 0:
   pi.wave_send_repeat(wid)
   time.sleep(5)
   pi.wave_tx_stop()
   pi.wave_delete(wid)

   pi.write(GPIO, 0)
   pi.write(GPIO2, 0)
pi.write(GPIO, 0)
pi.write(GPIO2, 0)
pi.stop()
