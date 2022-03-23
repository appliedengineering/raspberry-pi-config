import pynmea2
import serial
import time
import msgpack

ser = serial.Serial(
     port="/dev/serial0",
     baudrate=115200,
     timeout=0
)

print("connected to: " + ser.portstr)

try:
   while True:
      raw = ser.readline()
      if (raw.startswith(b"$GPGGA")):
         msg = pynmea2.parse(raw.decode("utf-8"))
         print("%s, %s" % (msg.lat, msg.lon))
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
