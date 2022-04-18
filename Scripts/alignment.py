import concurrent.futures
import logging
import msgpack
import threading
import traceback
import zmq
import time

import compassmodule
import servodriver
import gpsdriver
import alignmentcalc
import zmqdriver

# Set logging verbosity
# CRITICAL will not log anything
# ERROR will only log exceptions
# INFO will log more information
log_level = logging.INFO

compass = compassmodule.compassmodule("/dev/ttyACM0", 9600)
servo = servodriver.servodriver(26, 0.15)
gps = gpsdriver.gpsdriver("/dev/serial0", 115200)
zmq = zmqdriver.zmqdriver("192.168.3.2") # 192.168.3.2 for atomic pi
alignmentc = alignmentcalc.alignmentcalc()

## Env Vars

acceptableError = 10 # in degrees
targetHeading = 0.0 # shared var between two threads

##

def alignmentThread(exit_event):
   while not exit_event.is_set():
      try:
         heading = compass.read()
         logging.info(heading, targetHeading)

         headingDelta = heading - targetHeading

         if abs(headingDelta) > 180:
            if headingDelta < 0:
               headingDelta += 360
            else:
               headingDelta -= 360

         if abs(headingDelta) > acceptableError:
            if headingDelta < 0:
               servo.turnCW()
            elif headingDelta > 0:
               servo.turnCCW()
         else:
            servo.stop()

      except:
         traceback.print_exc()
         exit_event.set()
      time.sleep(0.01)

##

def positioningThread(exit_event):
   while not exit_event.is_set():
      try:
         boatC = gps.getCoordinates() # lat, lon
         zmq.transmitPosition(boatC[0], boatC[1])

         groundC = zmq.receivePosition() # lat, lon
         
         if len(boatC) != 2 or len(groundC) != 2:
            print(f"INVALID COORDINATES IN POS THREAD - {len(boatC)} : {len(groundC)}")
            continue
         
         targetHeading = alignmentc.getAngle(boatC[0], boatC[1], groundC[0], groundC[1])

      except:
         traceback.print_exc()
         exit_event.set()
      time.sleep(0.01)

###

if __name__ == '__main__':
   try:
      logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=log_level, datefmt="%H:%M:%S")

      exit_event = threading.Event()

      with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
         executor.submit(alignmentThread, exit_event)
         executor.submit(positioningThread, exit_event)

   except KeyboardInterrupt:
      logging.info('Setting exit event.')
      exit_event.set()
   except:
      traceback.print_exc()
      exit_event.set()
