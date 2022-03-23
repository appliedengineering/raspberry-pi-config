
import smbus
import time
import math

bus = smbus.SMBus(4) # 23 is SDA, 24 is SCL
#bus.pec = 1

def writeByte(addr, reg, data):
   bus.write_byte_data(addr, reg, data)
   time.sleep(0.1)

magAddr = 0x0d
accAddr = 0x19

# Magnetometer Register Offsets

#CRA_REG_M = 0x00
#MR_REG_M = 0x02
REG_STATUS_1 = 0x06

REG_CONTROL_1 = 0x09
REG_CONTROL_2 = 0x0a

REG_RST_PERIOD = 0x0b

INT_ENB = 0b00000001

SOFT_RST = 0b10000000

MODE_STBY = 0b00000000
MODE_CONT = 0b00000001

# Turn on Magnetometer

writeByte(magAddr, REG_CONTROL_2, SOFT_RST)
writeByte(magAddr, REG_CONTROL_2, INT_ENB)
writeByte(magAddr, REG_RST_PERIOD, 0x01)
writeByte(magAddr, REG_CONTROL_1, MODE_CONT)
#bus.write_byte_data(magAddr, CRA_REG_M, 0x14) # Mag sensor ODR from 15 Hz to 30 Hz
#bus.write_byte_data(magAddr, MR_REG_M, 0x01) # Mag sensor config from sleep mode to cont. mode

#print(bus.read_byte_data(magAddr, MR_REG_M))

try:
  while True:
    print(bus.read_byte_data(magAddr, REG_STATUS_1))
    #x1 = bus.read_byte_data(magAddr, 0x00)
    #x2 = bus.read_byte_data(magAddr, 0x01)
    #print((x1 * 256) + x2)
    print("x-", bus.read_byte_data(magAddr, 0x00), " y-", bus.read_byte_data(magAddr, 0x02), " z-", bus.read_byte_data(magAddr, 0x04))
#    ptr = bus.read_byte_data(magAddr, MR_REG_M)
#    print(ptr)
#    print(bus.read_byte_data(magAddr, ptr))
    time.sleep(0.1)
except KeyboardInterrupt:
  print("exit")

bus.close()
