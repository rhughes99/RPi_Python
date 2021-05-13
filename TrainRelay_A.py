# Train input and relay control
#  Uses Adafruit MCP23017 package (I2C) for input
#   and smbus (I2C) for output (relay control)

import time
import smbus

import board
import busio
import digitalio

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

bus = smbus.SMBus(1)
# All relay module address switches off
busAddress = 0x27
relayCmd = bus.read_byte(busAddress)
print("Relay Module Start: 0x%X" % (relayCmd))

while True:
    try:
        pin0.value = True
#        bus.write_byte(busAddress, 0xFF)
        print('LED Off')
        time.sleep(1)
        
        pin0.value = False
#        bus.write_byte(busAddress, 0xFE)
        print('LED On')
#        time.sleep(1)
        
#        print("Pin 1 is at a high level:{0}".format(pin1.value))
        if pin1.value:
            print('Pin 1 off')
            relayCmd |= 0b00000001
            bus.write_byte(busAddress, relayCmd)
        else:
            print('Pin 1 ON')
            relayCmd &= 0b11111110
            bus.write_byte(busAddress, relayCmd)
        
#        print("Pin 2 is at a high level:{0}".format(pin2.value))
        if pin2.value:
            print('Pin 2 off')
            relayCmd |= 0b00000010
            bus.write_byte(busAddress, relayCmd)
        else:
            print('Pin 2 ON')
            relayCmd &= 0b11111101
            bus.write_byte(busAddress, relayCmd)
                
        time.sleep(1)
        print('')
    
    except KeyboardInterrupt as ki:
        bus.write_byte(busAddress, 0xFF)
        print('-------')
        print('Exiting...')
        break

