import pynmea2
import serial
import time

class gpsdriver:
   def __init__(self, p, b): #/dev/serial0, 115200
      self.ser = serial.Serial(port=p, baudrate=b, timeout=0)

   def __readSer(self):
      return self.ser.readline()

   def getCoordinates(self): # lat, lon
      raw = self.__readSer()
      if (raw.startswith(b"$GPGGA")):
          try:
              msg = pynmea2.parse(raw.decode("utf-8"))
          except:
              print("FAILED TO PARSE GPS DATA")
              return -1.0, -1.0
          return msg.latitude, msg.longitude
      return 0.0, 0.0
