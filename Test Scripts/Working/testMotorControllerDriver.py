import time
import serial
import msgpack

mtrctrlSer = serial.Serial(
	port="/dev/ttyUSB0",
	baudrate=115200,
)

_ = mtrctrlSer.readline() # throw away first read
_2 = mtrctrlSer.readline() # throw away second read

#print("after first two reads")

test = 5

try:
   while True:
      raw = mtrctrlSer.readline()
      raw = raw[:-4]
      #print(raw)
      print(msgpack.unpackb(raw))
      #print(mtrctrlSer.readline())
      test = 5 - test
      print(test)
      r = str(test) + "\n"
      mtrctrlSer.write(r.encode())
      time.sleep(2)
except Exception as e:
   print(e)
except KeyboardInterrupt:
   print("exit")
