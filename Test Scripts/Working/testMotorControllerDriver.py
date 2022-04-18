import time
import serial
import msgpack

mtrctrlSer = serial.Serial(
	port="/dev/ttyUSB0",
	baudrate=9600,
)

_ = mtrctrlSer.readline() # throw away first read
_2 = mtrctrlSer.readline() # throw away second read

#print("after first two reads")

try:
   while True:
       try:
           raw = mtrctrlSer.readline()
           raw = raw[:-4]
#           print(raw)
           print(msgpack.unpackb(raw))
#     print(mtrctrlSer.readline())
           time.sleep(0.1)
       except Exception:
           print("corrupted data recieved")

except KeyboardInterrupt:
   print("exit")
