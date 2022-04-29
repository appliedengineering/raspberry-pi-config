import time
import serial
import msgpack

class motorcontrollerdriver:
    def __init__(self, p, b = 9600): # "/dev/ttyUSB0", 9600
        self.__mtrctrlSer = serial.Serial(
	        port=p,
	        baudrate = b,
        )
        _ = self.__mtrctrlSer.readline() # throw away first read
        _2 = self.__mtrctrlSer.readline() # throw away second read

    def read(self):
        try:
            raw = self.__mtrctrlSer.readline()
            return raw[:-4]
        except Exception:
            print("corrupted data recv")
        return dict()

    def sendMotorStatus(self, isOn):
        d = 0
        if isOn:
            d = 5
        try:
            #print(d)
            self.__mtrctrlSer.send(d + "\r\n")
        except Exception:
            print("Unable to send motor controller status")
            return False
        return True

