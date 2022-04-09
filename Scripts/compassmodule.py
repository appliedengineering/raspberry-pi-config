import serial
import time

class compassmodule:
   def __init__(self, port, baudrate):
      self.ser = serial.Serial(port, baudrate)

   def __readSer(self):
      return self.ser.readline()

   def __castToFloat(self, raw):
      f = 0.0
      try:
        f = float(raw)
      except:
        f = 0.0
      return f

   def read(self):
      raw = self.__readSer()
      return self.__castToFloat(raw)
