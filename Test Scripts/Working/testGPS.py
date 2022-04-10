import pynmea2
import serial
import time
import msgpack
import math

ser = serial.Serial(
     port="/dev/serial0",
     baudrate=115200,
     timeout=0
)

print("connected to: " + ser.portstr)

def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

def truncateWholeNumbers(f):
   return f - int(f)

def convertCoordinate(strC, strD):
   if not len(strC):
     print("FAILED TO CONVERT COORDINATE")
     return 0.0
   c = float(strC)
   deg = int(c / 100)
   min = int(c) % 100
   sec = truncate(truncateWholeNumbers(c) * 100, 7)
#   print(deg, min, sec)
   coord = deg + min/60 + sec/3600

   if(strD == 'S' or strD == 'W'):
     coord = -coord
   return coord

try:
   while True:
      raw = ser.readline()
#      if len(raw) > 0:
#          print(raw)
      if (raw.startswith(b"$GPGGA")):
         msg = pynmea2.parse(raw.decode("utf-8"))
         print(msg.lat, msg.lon)

         if (len(msg.lat) < 0 or len(msg.lon) < 0): # invalid data parsed
            continue

         lat = convertCoordinate(msg.lat, msg.lat_dir)
         lon = convertCoordinate(msg.lon, msg.lon_dir)
         print(lat, lon)

      time.sleep(0.01)
except KeyboardInterrupt:
   print("exit")

#this will store the line
#seq = []
#count = 1
#lat = ''
#lon = ''

# creates string of raw NMEA data
#while True:
#    for c in ser.read():
#        seq.append(chr(c)) # convert from ASCII
#        joined_seq = ''.join(str(v) for v in seq) # Make a string from array
#
#        if chr(c) == '\n':
#            msg = pynmea2.parse(joined_seq)
#            if( joined_seq.find(',N') != -1 and joined_seq.find('000.0') == -1 and join_seq.find(',,,') == -1):
#                try:
#                    print(msg.latitude)
#                    print(msg.longitude)
#
#                except AttributeError:
#                    pass
#            #print(msg)
#            seq = []
#            count += 1
#            break

#ser.close()
