import time
import serial
import msgpack

class motorcontrollerdriver:
    __isMotorControllerOn = False

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

    def updateMotorStatus(self, isOn):
        if isOn != self.__isMotorControllerOn:
           self.__isMotorControllerOn = isOn
        return self.sendMotorStatus()

    def sendMotorStatus(self):
        d = 0 # 0 is off
        if self.__isMotorControllerOn:
           d = 5 # 5 is on
        try:
           r = str(d) + "\n"
           print("sending to mtrctrl: ", r)
           self.__mtrctrlSer.write(r.encode())
        except Exception as e:
           print(e)
           return False
        return True
