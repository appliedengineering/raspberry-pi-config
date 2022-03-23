from gpiozero import Servo
import serial
import time

# Serial setup: port is /dev/ttyS0 if uart
ard = serial.Serial("/dev/ttyUSB0", 9600)

# Servo setup
mxp = 0.0025
mnp = 0.0004

servo = Servo(26, min_pulse_width=mnp, max_pulse_width=mxp)

# Variables

targetDeg = 100
acceptableError = 10 # in degrees

###

try:
   while True:
      rawHeading = ard.readline()
      heading = float(rawHeading)

      print(heading, targetDeg)

      headingDelta = heading - targetDeg

      if abs(headingDelta) > acceptableError:
         if headingDelta < 0:
            servo.max()
         elif headingDelta > 0:
            servo.min()
      else:
         servo.mid()

except KeyboardInterrupt:
      print("exit")
