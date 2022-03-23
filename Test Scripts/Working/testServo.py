from gpiozero import Servo
from time import sleep

mxp = 0.0025
mnp = 0.0004

servo = Servo(26, min_pulse_width=mnp, max_pulse_width=mxp)

print(servo.max_pulse_width)
print(servo.min_pulse_width)

#servo.value = 0.5
#print("mid")
#p = 1.0

t = 5

try:
   while True:
       servo.min()
       print("counterclockwise")
       sleep(t)

       servo.max()
       print("clockwise")
       sleep(t)

       #servo.value = -0.1
       servo.mid()
       print("stop")
       sleep(t)

except KeyboardInterrupt:
   print("keyboard")

