# MCP23017 test

import time

import board
import busio
import digitalio
#from digitalio import Direction

from adafruit_mcp230xx.mcp23017 import MCP23017
i2c = busio.I2C(board.SCL, board.SDA)

# MCP23017(i2c) defaults to address 0x20
mcp = MCP23017(i2c, address=0x20)

# LED connected to GPA0, actvie low
pin0 = mcp.get_pin(0)
pin0.direction = digitalio.Direction.OUTPUT

pin1 = mcp.get_pin(1)
pin1.direction = digitalio.Direction.INPUT
pin1.pull = digitalio.Pull.UP

pin2 = mcp.get_pin(2)
pin2.direction = digitalio.Direction.INPUT
pin2.pull = digitalio.Pull.UP

while True:
    try:
        pin0.value = True
        print('Off')
        time.sleep(2)
        
        pin0.value = False
        print('On')
        time.sleep(2)
        
        print("Pin 1 is at a high level:{0}".format(pin1.value))
        print("Pin 2 is at a high level:{0}".format(pin2.value))
        time.sleep(1)
        print('')
    
    except KeyboardInterrupt as ki:
        print('-----')
        print('Exiting...')
        break

