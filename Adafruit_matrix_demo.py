# Simple HT16K33 matrix controler example
# From Adafruit

# Import all board pins
import time
import board
import busio

# Import HT16K33 LED matrix module
from adafruit_ht16k33 import matrix

# Create I2C interface
i2c = busio.I2C(board.SCL, board.SDA)

# Create matrix class
# !!! These default to I2C address 0x70
#  16x8 matrix
# matrix = matrix.Matrix16x8(i2c)
#  16x8 matrix backpack
# matrix = matrix.MatrixBackpack16x8(i2c)
#  8x8 matrix
# matrix = matrix.Matrix8x8(i2c)
#  8x8 bicolor matrix
# matrix = matrix.Matrix8x8x2(i2c)

# Specify I2C HT16K33 address
matrix = matrix.Matrix8x8(i2c, address=0x71)

# Clear matrix
matrix.fill(0)

# Set pixel at origin (0, 0)
matrix[0, 0] = 1
# Set pixels in middle
matrix[3, 3] = 1
matrix[3, 4] = 1
matrix[4, 3] = 1
matrix[4, 4] = 1
# Set pixel in far corner
matrix[7, 7] = 1

time.sleep(2)

# Draw a Smiley Face
matrix.fill(0)

for row in range(2, 6):
    matrix[row, 0] = 1
    matrix[row, 7] = 1

for column in range(2, 6):
    matrix[0, column] = 1
    matrix[7, column] = 1

matrix[1, 1] = 1
matrix[1, 6] = 1
matrix[6, 1] = 1
matrix[6, 6] = 1
matrix[2, 5] = 1
matrix[5, 5] = 1
matrix[2, 3] = 1
matrix[5, 3] = 1
matrix[3, 2] = 1
matrix[4, 2] = 1

# Move Face around
while True:
    for row in range(2, 6):
        matrix[row, 0] = 1
        matrix[row, 7] = 1

    for column in range(2, 6):
        matrix[0, column] = 1
        matrix[7, column] = 1

    matrix[1, 1] = 1
    matrix[1, 6] = 1
    matrix[6, 1] = 1
    matrix[6, 6] = 1
    matrix[2, 5] = 1
    matrix[5, 5] = 1
    matrix[2, 3] = 1
    matrix[5, 3] = 1
    matrix[3, 2] = 1
    matrix[4, 2] = 1
    time.sleep(2)
    
    for frame in range(0, 8):
        matrix.shift_right(True)
        time.sleep(0.5)
    time.sleep(1)
    
    for frame in range(0, 8):
        matrix.shift_down(True)
        time.sleep(0.5)
    time.sleep(1)
    
    for frame in range(0, 8):
        matrix.shift_left(True)
        time.sleep(0.5)
    time.sleep(1)
    
    for frame in range(0, 8):
        matrix.shift_up(True)
        time.sleep(0.5)
    time.sleep(1)
    
    matrix.fill(1)
    time.sleep(1)
    matrix.fill(0)
    time.sleep(1)
    
