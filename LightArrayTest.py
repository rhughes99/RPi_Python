# LightArrayTest
#  Test routine for Uncle Jim's light array
#  22 lights, numbered 21 - 0, from right to left
#   Lights 15:0 are 'standard' white [16]
#   Light 16 is 'standard' red [1]
#   Lights 18:17 are 'standard' white, 'standard' spares? [2]
#   Lights 21:19 are 'high voltage' white, will appear dim [3]

import smbus
import time
import random

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
		# Lights 7:0
		if value <= 0x000080:
			shiftedValue = value
			bus.write_byte_data(DEVICE0, GPIOA, shiftedValue)
			bus.write_byte_data(DEVICE0, GPIOB, 0)
			bus.write_byte_data(DEVICE1, GPIOA, 0)
#			bus.write_byte_data(DEVICE1, GPIOB, 0)

		# Lights 15:8
		elif value <= 0x008000:
			shiftedValue = value >> 8
			bus.write_byte_data(DEVICE0, GPIOA, 0)
			bus.write_byte_data(DEVICE0, GPIOB, shiftedValue)
			bus.write_byte_data(DEVICE1, GPIOA, 0)
#			bus.write_byte_data(DEVICE1, GPIOB, 0)

		# Lights 21:16
		elif value <= 0x800000:
			shiftedValue = value >> 16
			bus.write_byte_data(DEVICE0, GPIOA, 0)
			bus.write_byte_data(DEVICE0, GPIOB, 0)
			bus.write_byte_data(DEVICE1, GPIOA, shiftedValue)
#			bus.write_byte_data(DEVICE1, GPIOB, 0)

		else:
			print('Should not be here')
			shiftedValue = value >> 24
			bus.write_byte_data(DEVICE0, GPIOA, 0)
			bus.write_byte_data(DEVICE0, GPIOB, 0)
			bus.write_byte_data(DEVICE1, GPIOA, 0)
			bus.write_byte_data(DEVICE1, GPIOB, shiftedValue)

#		print('value =', bin(value))

		value = value << 1
		if value == 0x20000:
			value = 1
#			print('Recycle...')

		# Random patterns for lights 15:00
		#  Simulating 1950's computer display
		bus.write_byte_data(DEVICE0, GPIOA, random.randint(0,255))
		bus.write_byte_data(DEVICE0, GPIOB, random.randint(0,255))

		time.sleep(1.0)

	except KeyboardInterrupt as ki:
		bus.write_byte_data(DEVICE0, GPIOA, 0)
		bus.write_byte_data(DEVICE0, GPIOB, 0)
		bus.write_byte_data(DEVICE1, GPIOA, 0)
#		bus.write_byte_data(DEVICE1, GPIOB, 0)

		print('Exiting...')
		break
