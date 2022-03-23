import time
import board
import adafruit_adxl34x

i2c = board.I2C()

acc = adafruit_adxl34x.ADXL343(i2c)

while True:
    print(acc.acceleration)
    time.sleep(0.1)
