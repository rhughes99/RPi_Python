# Exploring HT16K33 matrix functions

import board
import busio as io
import adafruit_ht16k33.matrix

from time import sleep

# Initialize I2C bus
i2c = io.I2C(board.SCL, board.SDA)

#matrix = adafruit_ht16k33.matrix.Matrix8x8(i2c)
matrix = adafruit_ht16k33.matrix.Matrix8x8(i2c, address=0x71)

# By default, display updates automatically
# matrix.auto_write = False
# matrix.show()

matrix.fill(1)
sleep(2)
matrix.fill(0)
sleep(2)

#matrix[7, 7] = 1
matrix[3, 3] = 1
matrix[0, 1] = 1

# 0.0 -> 1.0
matrix.brightness = 0.5
sleep(2)

# 0 = no blinking
# 1 = fast
# 2 = moderate
# 3 = slow
matrix.blink_rate = 2


