from gpiozero import Servo
from time import sleep

class servodriver:
   __mxp = 0.0024
   __mnp = 0.0004

   s = Servo(17) # default pin that is going to be replaced later
   sp = 0.2 # value from 0 to 1.0 that determines the speed the motor turns at - closer to 1 means faster

   def __init__(self, pin, speed):
     self.s = Servo(pin, min_pulse_width=self.__mnp, max_pulse_width=self.__mxp)
     self.sp = speed

   def turnCW(self):
     self.s.value = self.sp

   def turnCCW(self):
     self.s.value = -self.sp

   def stop(self):
     self.s.mid()
