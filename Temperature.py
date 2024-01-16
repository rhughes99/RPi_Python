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
# Sensor 6 (0xBC0000043EFFC128) - Outside temperature,
romCode = [ [0x28,0x52,0x86,0xAA,0x03,0x00,0x00,0x5F],
			[0x28,0x8A,0x61,0xAA,0x03,0x00,0x00,0xB1],
			[0x28,0x2E,0x89,0xAA,0x03,0x00,0x00,0xD5],
			[0x28,0xC2,0xAB,0xAA,0x03,0x00,0x00,0xFA],
			[0x28,0x6E,0xAA,0xAA,0x03,0x00,0x00,0x16],
			[0x28,0xEB,0x72,0xAA,0x03,0x00,0x00,0x77],
			[0x28,0xC1,0xFF,0x3E,0x04,0x00,0x00,0xBC] ]

#----------------------------------------------
def DS2482_deviceReset():
	# Performs global reset of device state machine; terminates any ongoing 1-Wire communication
	# Restriction: None
	# Read Pointer Position: Status Register
	# Status Bits Affected: RST = 1; 1WB = PPD = SD = SBR = TSB = DIR = 0
	# Configuration Bits Affected: 1WS = APU = SPU = 0
	# Returns True if device reset, False if problem or no device

	bus.write_byte(tempSenseAddr, 0xF0)
	status = bus.read_byte(tempSenseAddr)
#	print('[DS2482_deviceReset] status = {}' .format(bin(status)))

	if status & 0xF7 == DS2482_STATUS_RST:	# RST = 1 after executing Device Reset
		return True
	else:
		print('*** Error in DS2482_deviceReset: incorrect read back of status')
		return False

#----------------------------------------------
def DS2482_setReadPointer(ptrCode):
	# Sets read pointer to specified register
	# Restriction: None
	# Read Pointer Position: As specified by ptrCode
	# Status Bits Affected: None
	# Configuration Bits Affected: None

#	print('in DS2482_setReadPointer()')
	bus.write_i2c_block_data(tempSenseAddr, 0xE1, [ptrCode])

#----------------------------------------------
def DS2482_writeConfiguration(config):
	# Writes new configuration, settings take effect immediately
	# Restriction: 1-Wire activity must have ended (1WB = 0)
	# Read Pointer Position: Configuration Register
	# Status Bits Affected: RST = 0
	# Configuration Bits Affected: 1WS, SPU & APU updated
	# Returns True if success, False if problem

#	print('in DS2482_writeConfiguration()')
	WaitForOWBusAvailable()
	c = config | (~config<<4)
	bus.write_byte_data(tempSenseAddr, 0xD2, c)
	status = bus.read_byte(tempSenseAddr)
#	print('[DS2482_writeConfiguration] status =', bin(status))

	if status == config:
		return True
	else:
		print('*** Error in DS2482_writeConfiguration: incorrect read back of config')
		return False

#----------------------------------------------
def DS2482_owReset():
	# Generates 1-Wire reset/presence-detect cycle
	# Restriction: 1-Wire activity must have ended (1WB = 0)
	# Duration: 1.25 ms
	# Read Pointer Position: Status Register
	# Status Bits Affected: 1WB, PPD, SD
	# Configuration Bits Affected: 1WS, APU, SPU
	# Returns True if no issue, False if problem or no device

#	print('in DS2482_owReset()')
	WaitForOWBusAvailable()

	bus.write_byte(tempSenseAddr, 0xB4)
	time.sleep(0.002)

	data = bus.read_byte(tempSenseAddr)
	if data & DS2482_STATUS_SD:
		print('*** DS2482_owReset: 1-Wire short detected')
		return False

	if data & DS2482_STATUS_PPD == 0:
		print('*** DS2482_owReset: 1-Wire presence pulse not detected')
		return False

	return True

#----------------------------------------------
def DS2482_owWriteByte(data):
	# Writes single byte to 1-Wire line
	# Restriction: 1-Wire activity must have ended (1WB = 0)
	# Read Pointer Position: Status Register
	# Status Bits Affected: 1WB (set to 1 for 8 x tSLOT)
	# Configuration Bits Affected: 1WS, APU, SPU

#	print('in DS2482_owWriteByte()')
	WaitForOWBusAvailable()
	bus.write_byte_data(tempSenseAddr, 0xA5, data)

#----------------------------------------------
def DS2482_owReadByte():
	# Generates eight read-data time slots on 1-Wire line
	# Restriction: 1-Wire activity must have ended (1WB = 0)
	# Read Pointer Position: Status Register
	#	Note: To read data byte received from 1-Wire line, issue
	#	Set Read Pointer command and select the Read Data Register.
	#	Then access DS2482-100 in read mode.
	# Status Bits Affected: 1WB (set to 1 for 8 x tSLOT)
	# Configuration Bits Affected: 1WS, APU

#	print('in DS2482_owReadByte')
	WaitForOWBusAvailable()
	bus.write_byte(tempSenseAddr, 0x96)		# 1-Wire Read Byte

#----------------------------------------------
def DS2482_readStatusRegister():
	# Reads DS2482 Status Register and reports results
	# Assumes we are already pointing at Status Register

#	print('in DS2482_readStatusRegister()')
	status = bus.read_byte(tempSenseAddr)
	print('---------- Status ----------')
	if status & DS2482_STATUS_1WB == 1:
		print('1WB = 1: 1-Wire is busy')
	else:
		print('1WB = 0: 1-Wire is not busy')

	if status & DS2482_STATUS_PPD == 1:
		print('PPD = 1: Presence pulse detected')
	else:
		print('PPD = 0: Presence pulse not detected')

	if status & DS2482_STATUS_SD == 1:
		print('SD = 1: Short detected')
	else:
		print('SD = 0: Short not detected')

	if status & DS2482_STATUS_LL == 1:
		print('LL = 1')
	else:
		print('LL = 0')

	if status & DS2482_STATUS_RST == 1:
		print('RST = 1: DS2482 has performed internal reset cycle')
	else:
		status('RST = 0: Write Configuration command executed')

	if status & DS2482_STATUS_SBR == 1:
		print('SBR (Single Bit Result) = 1')
	else:
		print('SBR (Single Bit Result) = 0')

	if status & DS2482_STATUS_TSB == 1:
		print('TSB (Triple Second Bit) = 1')
	else:
		print('TSB (Triple Second Bit) = 0')

	if status & DS2482_STATUS_DIR == 1:
		print('DIR (Branch Direction Taken) = 1')
	else:
		print('DIR (Branch Direction Taken) = 0')

#----------------------------------------------
def WaitForOWBusAvailable():
	# Reads DS2482 Status Register and returns when 1-Wire bus is not busy
	# or if cycle count exceeds threshold

#	print('in waitForOWBusAvailable()')
	cycles = 0
	stillWaiting = True
	DS2482_setReadPointer(DS2482_STATUS_REG)
	while stillWaiting:
		data = bus.read_byte(tempSenseAddr)
		if data & DS2482_STATUS_1WB:
			stillWaiting = True
		else:
			stillWaiting = False

		cycles = cycles + 1
		if cycles > 10:
			print('*** WaitForOWBusAvailable(): cycles > 10')
			stillWaiting = False

#----------------------------------------------
def DS18B20_initiateReadTemperature():
	# Initiates temperature conversion for all sensors
	#  Send 1-Wire Reset
	#  Send Skip ROM command (address all 1-Wire devices)
	#  Send Convert T command
	#  Sleep for temperature conversion period

	DS2482_owReset()

	# Send DS18B20 Skip ROM command
	DS2482_owWriteByte(0xCC)

	# Send DS18B20 Convert T command
	DS2482_owWriteByte(0x44)

	# Capture and display conversion time
	# TIME STUFF

	# Wait for temperature conversion (750 ms for 12 bits)
	time.sleep(0.750)
	DS18B20_finishReadTemperature()

#----------------------------------------------
def DS18B20_finishReadTemperature():
	# Individually reads temperature from each connected sensor
	#  Send 1-Wire Reset
	#  Send Match ROM command
	#  Send Read Scratchpad command
	#  Repeat 9 times
	#    Repeat 8 times
	#    Send 1-Wire Read Byte command
	#    Set DS2482 read pointer to Data Register
	#    Read byte from DS2482
	#  Convert data to temperature

#	print('in DS18B20_finishReadTemperature')
	scratchPad = []
	for sensor in range(NUM_TEMP_SENSORS):
		# All DS18B20 transctons start with initialization (reset OW bus)
		DS2482_owReset()

		# Send DS18B20 Match ROM command
		DS2482_owWriteByte(0x55)		# DS18B20 Match ROM

		# Send 8 bytes of ROM code
		for i in range(8):
#			print('romCode: ', hex(romCode[sensor][i]))
			DS2482_owWriteByte(romCode[sensor][i])

		# Send DS18B20 Read Scratchpad command
		DS2482_owWriteByte(0xBE)		# DS18B20 Read Scratchpad

		crc8 = 0
		scratchPad.clear()
		# Read 9 bytes of scratchPad
		for i in range(9):
			DS2482_owReadByte()

			# Set read pointer
			DS2482_setReadPointer(DS2482_READ_DATA_REG)

			# Read byte from DS2482
			data = bus.read_byte(tempSenseAddr)

			scratchPad.append(data)

			# crc8 is running crc calculation result
			crc8 = computeCRC(crc8, data)

		# Validate scratchPad data checksum
		if crc8 == 0:
			# Convert scratchpad bytes 0 (LSB) & 1 (MSB) to temperature
#			print(f'    scratchPad: {scratchPad}')
			temperatureDegC = (scratchPad[0] / 16.0) + (scratchPad[1] & 0x07) * 16.0
			if scratchPad[1] & 0x08:		# temperature <0 deg C
				temperatureDegC = temperatureDegC - 128.0

#			temperatureDegF[sampleIdx][sensor] = 9.0 / 5.0 * temperatureDegC + 32.0
#			message = f"DS18B20_finishReadTemperature: sensor {sensor}: temperatureDegF= {temperatureDegF[sampleIdx][sensor]}"
#			print(message)
#			print('DS18B20_finishReadTemperature: sensor %d: temperatureDegF = %.1f", sensor, temperatureDegF[sampleIdx][sensor]);

#			printTemperature(sensor, temperatureDegF)

			tempF = 9.0 / 5.0 * temperatureDegC + 32.0
#			print('tempF = ',tempF)
			printTemperature(sensor, tempF)

		else:
			print('*** Bad checksum')
			print(f'scratchPad: {scratchPad}')

		# Time tag stuff
		# Write data to file stuff

#----------------------------------------------
def computeCRC(crc8, inByte):
	crcTable = [0, 94, 188, 226, 97, 63, 221, 131, 194, 156, 126, 32, 163, 253, 31, 65,
				157, 195, 33, 127, 252, 162, 64, 30, 95, 1, 227, 189, 62, 96, 130, 220,
				35, 125, 159, 193, 66, 28, 254, 160, 225, 191, 93, 3, 128, 222, 60, 98,
				190, 224, 2, 92, 223, 129, 99, 61, 124, 34, 192, 158, 29, 67, 161, 255,
				70, 24, 250, 164, 39, 121, 155, 197, 132, 218, 56, 102, 229, 187, 89, 7,
				219, 133, 103, 57, 186, 228, 6, 88, 25, 71, 165, 251, 120, 38, 196, 154,
				101, 59, 217, 135, 4, 90, 184, 230, 167, 249, 27, 69, 198, 152, 122, 36,
				248, 166, 68, 26, 153, 199, 37, 123, 58, 100, 134, 216, 91, 5, 231, 185,
				140, 210, 48, 110, 237, 179, 81, 15, 78, 16, 242, 172, 47, 113, 147, 205,
				17, 79, 173, 243, 112, 46, 204, 146, 211, 141, 111, 49, 178, 236, 14, 80,
				175, 241, 19, 77, 206, 144, 114, 44, 109, 51, 209, 143, 12, 82, 176, 238,
				50, 108, 142, 208, 83, 13, 239, 177, 240, 174, 76, 18, 145, 207, 45, 115,
				202, 148, 118, 40, 171, 245, 23, 73, 8, 86, 180, 234, 105, 55, 213, 139,
				87, 9, 235, 181, 54, 104, 138, 212, 149, 203, 41, 119, 244, 170, 72, 22,
				233, 183, 85, 11, 136, 214, 52, 106, 43, 117, 151, 201, 74, 20, 246, 168,
				116, 42, 200, 150, 21, 75, 169, 247, 182, 232, 10, 84, 215, 137, 107, 53]

	return crcTable[crc8 ^ inByte]

#----------------------------------------------
def printTemperature(sensor, temperature):
	if sensor == 0:
		message = f"Basement Ambient: {temperature:.1f} degF"

	elif sensor == 1:
		message = f"Main Return: {temperature:.1f} degF"

	elif sensor == 2:
		message = f"Library Return: {temperature:.1f} degF"

	elif sensor == 3:
		message = f"Main Supply: {temperature:.1f} degF"

	elif sensor == 4:
		message = f"H20 Heater Input: {temperature:.1f} degF"

	elif sensor == 5:
		message = f"H20 Heater Output: {temperature:.1f} degF"

	elif sensor == 6:
		message = f"Outside: {temperature:.1f} degF"

	else:
		message = f"*** printTemperature(): Unexpected sensor {sensor}"

	print(message)


#----------------------------------------------
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
bus.write_byte(relayBdAddr, 0xFF)

# Turn LEDs off (outputs = 1)
blueLED.on()
greenLED.on()
redLED.on()
time.sleep(1)

# Cycle LEDs for fun
blueLED.off()
print('Blue')
time.sleep(1)
blueLED.on()

greenLED.off()
print('    Green')
time.sleep(1)
greenLED.on()

redLED.off()
print('         Red')
time.sleep(1)
redLED.on()


print('===================================')
print('Number of sensors:', NUM_TEMP_SENSORS)


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
#print('Reset OW bus')
i2cOK = DS2482_owReset()
if i2cOK:
	print('OW reset OK')

	i = 0
	while True:
		try:
			blueLED.on()
			redLED.off()
			print('-----------------------------------',i)
			DS18B20_initiateReadTemperature()
			redLED.on()
			blueLED.off()
			i = i+1
			time.sleep(5.0)

		except KeyboardInterrupt as ki:
			bus.write_byte(relayBdAddr, 0xFF)
			blueLED.on()
			greenLED.on()
			redLED.on()
			print('-------')
			print('Exiting...')
			break
else:
	print('Mission failure...')
