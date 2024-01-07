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
NUM_TEMP_SENSORS = 1		# number of 1-Wire sensors

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



def DS2482_deviceReset():
    bus.write_byte(tempSenseAddr, 0xF0)
    status = bus.read_byte(tempSenseAddr)
    print('[DS2482_deviceReset] status = %d' % status)

    if status & 0xF7 == DS2482_STATUS_RST:	# RST = 1 after executing Device Reset
        return True
    else:
        print('*** Error in DS2482_deviceReset: incorrect read back of status');
        return False

def DS2482_writeConfiguration(config):
    print('DS2482_writeConfiguration()')
    WaitForOWBusAvailable()


def WaitForOWBusAvailable():
    print('WaitForOWBusAvailable()')



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


i2cOK = DS2482_deviceReset()
if i2cOK:
	print('DS2482 reset OK')
else:
	print('*** DS2482 reset FAIL')


if NUM_TEMP_SENSORS > 1:
	i2cOK = DS2482_writeConfiguration(0x01)		# Active Pullup enabled
else:
	i2cOK = DS2482_writeConfiguration(0x00)		# Active Pullup disabled




while True:
    try:




        time.sleep(0.20)

    except KeyboardInterrupt as ki:
        print('-------')
        print('Exiting...')
        break
