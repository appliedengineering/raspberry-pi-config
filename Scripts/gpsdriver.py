import pynmea2
import serial
import time

class gpsdriver:
   __prevLat = 0.0
   __prevLon = 0.0

   def __init__(self, p, b): #/dev/serial0, 115200
      self.__ser = serial.Serial(port=p, baudrate=b, timeout=0)

   def __readSer(self):
      return self.__ser.readline()

   def getCoordinates(self): # lat, lon
      raw = self.__readSer()

#      timeoutC = 0
#      while timeoutC < 100 and not raw.startswith(b"$GPGGA"):
#          raw = self.__readSer()
#          print(raw)
#          timeoutC += 1
#         time.sleep(0.01)

      if (raw.startswith(b"$GPGGA") or raw.startswith(b"$GNRMC")):
          try:
              msg = pynmea2.parse(raw.decode("utf-8"))
              lat = msg.latitude
              lon = msg.longitude
          except:
              print("FAILED TO PARSE GPS DATA")
              return -1.0, -1.0
          self.__prevLat = lat
          self.__prevLon = lon
      return self.__prevLat, self.__prevLon
