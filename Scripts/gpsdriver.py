import pynmea2
import serial
import time

class gpsdriver:
   def __init__(self, p, b): #/dev/serial0, 115200
      self.__ser = serial.Serial(port=p, baudrate=b, timeout=0)

   def __readSer(self):
      return self.__ser.readline()

   def getCoordinates(self): # lat, lon
      raw = self.__readSer()
#      raw = self.__readSer()
 #     timeoutC = 0
 #     while timeoutC < 100 and not raw.startswith(b"$GPGGA"):
 #         raw = self.__readSer()
#          print(raw)
 #         timeoutC += 1
  #        time.sleep(0.01)

      if (raw.startswith(b"$GPGGA")):
          try:
              msg = pynmea2.parse(raw.decode("utf-8"))
              lat = msg.latitude
              lon = msg.longitude
          except:
              print("FAILED TO PARSE GPS DATA")
              return -1.0, -1.0
          return lat, lon
      return 0.0, 0.0
