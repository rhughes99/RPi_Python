# LightArrayTest
#  Test routine for Uncle Jim's light array
#  22 lights, numbered 21 - 0, from right to left
# 

import smbus
import time

bus = smbus.SMBus(1)

DEVICE0 = 0x21	# lights 15:00
DEVICE1 = 0x22	# lights 21:16

IODIRA = 0x00
IODIRB = 0x01
GPIOA  = 0x12
GPIOB  = 0x13

# Set MCP23017 pin directions, all output
bus.write_byte_data(DEVICE0, IODIRA, 0x00)
bus.write_byte_data(DEVICE0, IODIRB, 0x00)
bus.write_byte_data(DEVICE1, IODIRA, 0x00)
bus.write_byte_data(DEVICE1, IODIRB, 0x00)

value = 1
shiftedValue = 0

while True:
	try:
		if value <= 0x000080:
			shiftedValue = value
			bus.write_byte_data(DEVICE0, GPIOA, shiftedValue)
			bus.write_byte_data(DEVICE0, GPIOB, 0)
			bus.write_byte_data(DEVICE1, GPIOA, 0)
			bus.write_byte_data(DEVICE1, GPIOB, 0)
		
		elif value <= 0x008000:
			shiftedValue = value << 8
			bus.write_byte_data(DEVICE0, GPIOA, 0)
			bus.write_byte_data(DEVICE0, GPIOB, shiftedValue)
			bus.write_byte_data(DEVICE1, GPIOA, 0)
			bus.write_byte_data(DEVICE1, GPIOB, 0)
		
		elif value <= 0x800000:
			shiftedValue = value << 16
			bus.write_byte_data(DEVICE0, GPIOA, 0)
			bus.write_byte_data(DEVICE0, GPIOB, 0)
			bus.write_byte_data(DEVICE1, GPIOA, shiftedValue)
			bus.write_byte_data(DEVICE1, GPIOB, 0)

		else
			shiftedValue = value << 24
			bus.write_byte_data(DEVICE0, GPIOA, 0)
			bus.write_byte_data(DEVICE0, GPIOB, 0)
			bus.write_byte_data(DEVICE1, GPIOA, 0)
			bus.write_byte_data(DEVICE1, GPIOB, shiftedValue)

		print('shiftedValue' = {}' .format(bin(shiftedValue)))

		value = value << 1
		if value = 0x10000000:
			value = 1
		
		time.sleep(1.0)

    except KeyboardInterrupt as ki:
		bus.write_byte_data(DEVICE0, GPIOA, 0)
		bus.write_byte_data(DEVICE0, GPIOB, 0)
		bus.write_byte_data(DEVICE1, GPIOA, 0)
		bus.write_byte_data(DEVICE1, GPIOB, 0)

        print('Exiting...')
        break
