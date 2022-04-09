from gpiozero import Servo
from time import sleep

mxp = 0.0024 # 0.0025
mnp = 0.0004

servo = Servo(26, min_pulse_width=mnp, max_pulse_width=mxp)

print(servo.max_pulse_width)
print(servo.min_pulse_width)

#servo.value = 0.5
#print("mid")
#p = 1.0

t = 5
b = 0.2 # from 0 to 1.0, close to 1, the faster the servo turns

try:
   while True:
       servo.value = -b
       print("counterclockwise")
       sleep(t)

       servo.value = b
       print("clockwise")
       sleep(t)

       #servo.value = -0.1
       servo.value = 0
       print("stop")
       sleep(t)

except KeyboardInterrupt:
   print("keyboard")

