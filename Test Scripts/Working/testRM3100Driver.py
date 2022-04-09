import serial
import time
# port is /dev/ttyS0 if using uart /dev/ttyACM0 if using Arduino Uno
ser = serial.Serial("/dev/ttyACM0", 9600)
while True:
#	ser.write('M'.encode('utf-8'))
#	time.sleep(1)
	print("read")
	received_data = ser.readline()
	print(received_data)
	time.sleep(0.03)
