import time
import serial
import msgpack

mtrctrlSer = serial.Serial(
	port="/dev/ttyUSB0",
	baudrate=9600,
)

def readSer(a_serial, eol=b'\r\n'):
   leneol = len(eol)
   line = bytearray()
   while True:
      c = a_serial.read(1)
      if c:
         line += c
         if line[-leneol:] == eol:
            break
      else:
         break
   a_serial.reset_input_buffer()
   return bytes(line)

_ = readSer(mtrctrlSer) # throw away first read
_2 = readSer(mtrctrlSer) # throw away second read

#print("after first two reads")

test = 5

try:
   while True:
      raw = readSer(mtrctrlSer)
      print(raw)
      #print(msgpack.unpackb(raw))
      #print(mtrctrlSer.readline())
#      test = 5 - test
#      print(test)
#      r = str(test) + "\n"
#      mtrctrlSer.write(r.encode())
      time.sleep(0.01)
except Exception as e:
   print(e)
except KeyboardInterrupt:
   print("exit")
