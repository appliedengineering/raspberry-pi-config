
import smbus
import time
import math

bus = smbus.SMBus(4) # 23 is SDA, 24 is SCL
#bus.pec = 1

def writeByte(addr, reg, data):
   bus.write_byte_data(addr, reg, data)
   time.sleep(0.01)

def readByte(addr, reg):
   return bus.read_byte_data(addr, reg)

def convertDecToBinA(b):
   return [int(i) for i in list('{0:0b}'.format(b))]

def convertBinAToDec(b):
   return int("".join(str(x) for x in b), 2)

def convertTwosComp(raw):
   bin = convertDecToBinA(raw)

   bitCount = 16

   isNeg = (len(bin) == bitCount and bin[0] == 1)

   if not isNeg: # positive numbers are expressed correctly already
      return convertBinAToDec(bin)

   bin.pop(0) # remove polarity bit
   for i in range(len(bin)): # flip all bits
     bin[i] = 1-bin[i]
   t = (convertBinAToDec(bin) + 1) # add one
   return -t

def convertAxisToHeading(x, y):
   hRad = math.atan2(y, x)

   decDeg = 11
   decMin = 38
   declination = (decDeg + decMin / 60) * (math.pi / 180)

   hRad += declination

#   if (hRad < 0):
#     hRad += 2 * math.pi

#   if (hRad > 2 * math.pi):
#     hRad -= 2 * math.pi

   hDeg = hRad * 180 / math.pi
   return hDeg # ummm dont know why this works but it does...

#####

magAddr = 0x1e
accAddr = 0x19

# Magnetometer Register Offsets

CRA_REG_M = 0x00
CRB_REG_M = 0x01
MR_REG_M = 0x02

OUT_X_H_M = 0x03
OUT_X_L_M = 0x04
OUT_Z_H_M = 0x05
OUT_Z_L_M = 0x06
OUT_Y_H_M = 0x07
OUT_Y_L_M = 0x08

# Accelerometer Register Offsets

CTRL_REG1_A = 0x20
CTRL_REG4_A = 0x23

OUT_X_L_A = 0x28
OUT_X_H_A = 0x29
OUT_Y_L_A = 0x2A
OUT_Y_H_A = 0x2B
OUT_Z_L_A = 0x2C
OUT_Z_H_A = 0x2D

# Set up Magnetometer

writeByte(magAddr, MR_REG_M, 0x00) # Mag sensor config from sleep mode to cont. mode
writeByte(magAddr, CRA_REG_M, 0x14) # Temperature enabled, Data output rate = 15Hz 
writeByte(magAddr, CRB_REG_M, 0x20) # Gain configuration register = +/- 1.3

# Set up Accelerometer

writeByte(accAddr, CTRL_REG1_A, 0x27) # Normal operation mode with ODR 50Hz
writeByte(accAddr, CTRL_REG4_A, 0x40) # Full scale range +- 2 gauss + change to big-endian from little-endian

###

# Magnetometer auto-calibration vars
xMMin = None
xMMax = None
yMMin = None
yMMax = None

#print(convertTwosComp(6))

try:
  while True:

    x1 = readByte(magAddr, OUT_X_H_M)
    x2 = readByte(magAddr, OUT_X_L_M)
    z1 = readByte(magAddr, OUT_Z_H_M)
    z2 = readByte(magAddr, OUT_Z_L_M)
    y1 = readByte(magAddr, OUT_Y_H_M)
    y2 = readByte(magAddr, OUT_Y_L_M)

    x = convertTwosComp((x1 << 8) + x2)
    y = convertTwosComp((y1 << 8) + y2)
    z = convertTwosComp((z1 << 8) + z2)

#    print(x1, x2, y1, y2, z1, z2)
    if xMMin is None or x < xMMin:
       xMMin = x
    if xMMax is None or x > xMMax:
       xMMax = x
    if yMMin is None or y < yMMin:
       yMMin = y
    if yMMax is None or y > yMMax:
       yMMax = y

    xOff = (xMMax+xMMin)/2
    yOff = (yMMax+yMMin)/2

#    print(x, y, z, " : ", xOff, yOff, " = ", convertAxisToHeading(x, y))

    Ax1 = readByte(accAddr, OUT_X_L_A)
    Ax2 = readByte(accAddr, OUT_X_H_A)
    Ay1 = readByte(accAddr, OUT_Y_L_A)
    Ay2 = readByte(accAddr, OUT_Y_H_A)
    Az1 = readByte(accAddr, OUT_Z_L_A)
    Az2 = readByte(accAddr, OUT_Z_H_A)

    Ax = convertTwosComp((Ax1 << 8) + Ax2)
    Ay = convertTwosComp((Ay1 << 8) + Ay2)
    Az = convertTwosComp((Az1 << 8) + Az2)

    print(Ax, Ay, Az)

    time.sleep(0.1)
except KeyboardInterrupt:
  print("exit")

bus.close()
