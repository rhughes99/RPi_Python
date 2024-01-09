# Temperature
# Reads 1-Wire basement sensors
# Uses gpiozero for LEDs (for fun)
#  and smbus (I2C) for sensor input
#  DS2482-100 1-Wire Master

import time
#import random
import smbus
import gpiozero


# Pseudo Constants
NUM_TEMP_SENSORS = 7		# number of 1-Wire sensors

# DS2482-100 Valid Pointer Codes
DS2482_STATUS_REG    = 0xF0
DS2482_READ_DATA_REG = 0xE1
DS2482_CONFIG_REG    = 0xC3

# DS2482-100 Status Register Bit Assignments
DS2482_STATUS_1WB = 0x01	# 1-Wire Busy
DS2482_STATUS_PPD = 0x02	# Presence-Pulse Detect
DS2482_STATUS_SD  = 0x04	# Short Detected
DS2482_STATUS_LL  = 0x08	# Logic Level
DS2482_STATUS_RST = 0x10	# Device Reset
DS2482_STATUS_SBR = 0x20	# Single Bit Result
DS2482_STATUS_TSB = 0x40	# Triplet Second Bit
DS2482_STATUS_DIR = 0x80	# Branch Direction Taken

# Sensor ROM codes
# Sensor 0 (0x5F000003AA865228) - breadboard, basement ambient temperature
# Sensor 1 (0xB1000003AA618A28) - main house radiator return temperature
# Sensor 2 (0xD5000003AA892E28) - library radiator return temperature
# Sensor 3 (0xFA000003AAABC228) - radiator supply temperature
# Sensor 4 (0x77000003AA72EB28) - H20 heater input temperature
# Sensor 5 (0x16000003AAAA6E28) - H20 heater output temperature
# Sensor 6 (0xBC0000043EFFC128) - Outside temperature
romCode = [ [0x5F,0x00,0x00,0x03,0xAA,0x86,0x52,0x28], 
			[0xB1,0x00,0x00,0x03,0xAA,0x61,0x8A,0x28], 
			[0xD5,0x00,0x00,0x03,0xAA,0x89,0x2E,0x28], 
			[0xFA,0x00,0x00,0x03,0xAA,0xAB,0xC2,0x28], 
			[0x16,0x00,0x00,0x03,0xAA,0xAA,0x6E,0x28], 
			[0x77,0x00,0x00,0x03,0xAA,0x72,0xEB,0x28],
			[0xBC,0x00,0x00,0x04,0x3E,0xFF,0xC1,0x28] ]


def DS2482_deviceReset():
	# Performs global reset of device state machine; terminates any ongoing 1-Wire communication
	# Restriction: None
	# Read Pointer Position: Status Register
	# Status Bits Affected: RST = 1; 1WB = PPD = SD = SBR = TSB = DIR = 0
	# Configuration Bits Affected: 1WS = APU = SPU = 0
	# Returns True if device reset, False if problem or no device

    bus.write_byte(tempSenseAddr, 0xF0)
    status = bus.read_byte(tempSenseAddr)
    print('[DS2482_deviceReset] status = {}' .format(bin(status)))

    if status & 0xF7 == DS2482_STATUS_RST:	# RST = 1 after executing Device Reset
        return True
    else:
        print('*** Error in DS2482_deviceReset: incorrect read back of status');
        return False


def DS2482_writeConfiguration(config):
	# Writes new configuration, settings take effect immediately
	# Restriction: 1-Wire activity must have ended (1WB = 0)
	# Read Pointer Position: Configuration Register
	# Status Bits Affected: RST = 0
	# Configuration Bits Affected: 1WS, SPU & APU updated
	# Returns True if success, False if problem

	print('DS2482_writeConfiguration()')
	WaitForOWBusAvailable()
	bus.write_i2c_block(tempSenseAddr, 0xD2, config)
	status = bus.read_byte(tempSenseAddr)
	print('[DS2482_writeConfiguration] status = %b' % bin(status))

	if status == config:
		return True
	else:
		print('*** Error in DS2482_writeConfiguration: incorrect read back of config');
		return False


def WaitForOWBusAvailable():
	# Reads DS2482 Status Register and returns when 1-Wire bus is not busy
	# or if cycle count exceeds threshold

	print('WaitForOWBusAvailable()')
	cycles = 0
	stillWaiting = True
	DS2482_setReadPointer(DS2482_STATUS_REG)
	while stillWaiting:
#		data = DS2482_STATUS_1WB;	# set 1WBusy to busy
		data = bus.read_byte(tempSenseAddr)
		if data & DS2482_STATUS_1WB:
			stillWaiting = True
		else:
			stillWaiting = False

		cycles = cycles + 1
		if cycles > 10:
			print('*** WaitForOWBusAvailable(): cycles > 10')
			stillWaiting = False

def DS2482_owReset():
	# Generates 1-Wire reset/presence-detect cycle
	# Restriction: 1-Wire activity must have ended (1WB = 0)
	# Read Pointer Position: Status Register
	# Status Bits Affected: 1WB, PPD, SD
	# Configuration Bits Affected: 1WS, APU, SPU
	# Returns True if no issue, False if problem or no device

	WaitForOWBusAvailable()

	bus.write_byte(tempSenseAddr, 0xB4)
	# Loop while checking 1WB for completion of 1-Wire operation
	# Don't use waitForOWBusAvailable here because we want to
	#  check several status bits after waiting
	stillWaiting = True
	while stillWaiting:
		data = bus.read_byte(tempSenseAddr)
		if data & DS2482_STATUS_1WB:
			stillWaiting = True
		else:
			stillWaiting = False

		if data & DS2482_STATUS_SD:
			print('*** DS2482_owReset: 1-Wire short detected')

		if data & DS2482_STATUS_PPD == 0:
			print('*** DS2482_owReset: 1-Wire presence pulse not detected')

		return True




# GPIO assignments
# LEDs use negative logic, 0 = ON
blueLED  = gpiozero.LED(4)
greenLED = gpiozero.LED(17)
redLED   = gpiozero.LED(18)

# Not connected
in1 = gpiozero.Button(19)
in2 = gpiozero.Button(16)
in3 = gpiozero.Button(13)
in4 = gpiozero.Button(12)
in5 = gpiozero.Button(6)
in6 = gpiozero.Button(5)

# SMBus (I2C) setup
bus = smbus.SMBus(1)
tempSenseAddr = 0x18
relayBdAddr   = 0x27

# Turn all relays  off
bus.write_byte(relayBdAddr, 0x00)

# Turn LEDs off (outputs = 1)
blueLED.on()
greenLED.on()
redLED.on()
time.sleep(1)

# Cycle LEDs for fun
blueLED.off()
print('Blue')
time.sleep(2)
blueLED.on()

greenLED.off()
print('    Green')
time.sleep(2)
greenLED.on()

redLED.off()
print('         Red')
time.sleep(2)
redLED.on()


print('-----------------------------------')
print('Number of sensors: %d', NUM_TEMP_SENSORS)



i2cOK = DS2482_deviceReset()
if i2cOK:
	print('DS2482 reset OK')
else:
	print('*** DS2482 reset FAIL')

# Set active pullup
if NUM_TEMP_SENSORS > 1:
	i2cOK = DS2482_writeConfiguration(0x01)		# Active Pullup enabled
	print('Active pullup enabled')
else:
	i2cOK = DS2482_writeConfiguration(0x00)		# Active Pullup disabled
	print('Active pullup disabled')

# Reset OW bus
print('Reset OW bus')
i2cOK = DS2482_owReset()






while True:
	try:




		time.sleep(2.0)

	except KeyboardInterrupt as ki:
		bus.write_byte(relayBdAddr, 0x00)
		print('-------')
		print('Exiting...')
		break
