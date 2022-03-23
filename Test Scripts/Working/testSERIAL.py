import time
import serial

ser = serial.Serial(
	port="/dev/serial0",
	baudrate=115200,
	timeout=1.0
)

try:
    while True:
      print(ser.readline())
      time.sleep(0.5)
except KeyboardInterrupt:
    print("exit")
