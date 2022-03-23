import time
import RPi.GPIO as GPIO
import spidev

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz=1000

# PIN NUMBERS (PHYSICAL/BOARD)
MOSI = 19

# SETUP GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(MOSI, GPIO.IN)

# REGISTER ADDRS
READ_REG_OFFSET = 0x80 # RM3100 read offset

POLL_REG = 0x00
CCM_REG = 0x01
READ_REG = 0x24

def read(addr, size, offset = READ_REG_OFFSET):
   # prepareRead()
   spi.xfer([addr + offset])
   dataList = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
   # spi.xfer([addr+offset])
   #for x in range(0, size):
   return spi.xfer2(dataList)
   # newData = spi.readBytes(1)
   # dataList.extend(newData)
   # return dataList
   # return spi.readbytes(size)

def write(addr, val):
   spi.xfer2([(addr >> 1), val]) # RM3100 write offset

def prepareRead():
   write(POLL_REG, 0x70)
   # time.sleep(1)

###

def convertDecToBinA(b):
   return [int(i) for i in list('{0:0b}'.format(b))]

def convertBinAToDec(b):
   return int("".join(str(x) for x in b), 2)

def convertTwosComp(raw, bitCount = 16):
   bin = convertDecToBinA(raw)

#   print(bin)

   isNeg = (len(bin) == bitCount and bin[0] == 1) # MSB

   if not isNeg: # positive numbers are expressed correctly already
      return convertBinAToDec(bin)

   bin.pop(0)
   for i in range(len(bin)):
     bin[i] = 1-bin[i]
   t = (convertBinAToDec(bin) + 1) # add one
   return -t

####

print("starting read now")

# print(GPIO.input(19))

# prepareRead()

time.sleep(5)

try:
   while True:
      prepareRead()
      # while GPIO.input(19):
      time.sleep(1)

      raw = (read(READ_REG, 9))

      print(raw)

      rawX = (raw[0] << 16) + (raw[1] << 8) + raw[2] # first 3 bytes is for X
      rawY = (raw[3] << 16) + (raw[4] << 8) + raw[5]
      rawZ = (raw[6] << 16) + (raw[7] << 8) + raw[8]

#      print(rawX)

      x = convertTwosComp(rawX, 24)
      y = convertTwosComp(rawY, 24)
      z = convertTwosComp(rawZ, 24)

      print(x, y, z)

      time.sleep(0.1)
except KeyboardInterrupt:
   print("exit")
