# Demo using both I2C devices
# 11/14/2019

import board
import busio
import adafruit_mcp4725
import adafruit_ht16k33.matrix

from time import sleep

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize MCP4725 DAC
dac = adafruit_mcp4725.MCP4725(i2c, address=0x62)

# Initialize LED Matrix
matrix = adafruit_ht16k33.matrix.Matrix8x8(i2c, address=0x71)
matrix.fill(0)
matrix.brightness = 7    # 0 -> 15

matrixX = 0
matrixY = 0

def updateMatrix(x, y):
    matrix[x, y] = 0
    
    y = y + 1
    if y == 8:
        y = 0
        x = x + 1
        if x == 8:
            x = 0
    
    matrix[x, y] = 1
    return [x, y]

def arrowMatrix():
    matrix.fill(0)
    matrix.auto_write = False
    matrix[0,4] = 1
    matrix[1,3] = 1
    matrix[1,5] = 1
    matrix[2,2] = 1
    matrix[2,4] = 1
    matrix[2,6] = 1
    matrix[3,1] = 1
    matrix[3,4] = 1
    matrix[3,7] = 1
    matrix[4,4] = 1
    matrix[5,4] = 1
    matrix[6,4] = 1
    matrix[7,4] = 1
    matrix.show()
    matrix.auto_write = True


# Main loop goes up and down DAC range
while True:
#    print("Going up to 3.3 vdc...")
    for i in range(0, 4095, 1):
        dac.raw_value = i
        
        matrix.fill(0)
        if i % 5 == 0:
            arrowMatrix()
            sleep(1)
        
        else:
            [matrixX, matrixY] = updateMatrix(matrixX, matrixY)
            sleep(0.25)
        
#        [matrixX, matrixY] = updateMatrix(matrixX, matrixY)
#        matrix[5,4] = 1
#        arrowMatrix()
#        sleep(0.5)
    
#    print("Returning to 0 vdc...")
    for i in range(4095, -1, -1):
        dac.raw_value = i
        sleep(0.1)

