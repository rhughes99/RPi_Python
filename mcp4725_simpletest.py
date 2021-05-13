# Simple demo of setting DAC value up and down

import board
import busio
import adafruit_mcp4725

from time import sleep

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize MCP4725
#dac = adafruit_mcp4725.MCP4725(i2c)
dac = adafruit_mcp4725.MCP4725(i2c, address=0x62)


# Use value property with 16-bit number
# MCP4725 is 12-bit device so quantization errors will occur
#dac.value = nnn

# Directly read and write 12-bit DAC value
#dac.raw_value = nnn

# Use normalized value to set ouput with floating point value
# Range is 0 to 1
# dac.normalized_value = 0.3

step = 1

# Main loop goes up and down throough range
while True:
#    print("Going up to 3.3 vdc...")
    for i in range(0, 4095, step):
        dac.raw_value = i
        sleep(0.5)
    
#    print("Returning to 0 vdc...")
    for i in range(4095, -1, -step):
        dac.raw_value = i
        sleep(0.5)

