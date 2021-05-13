import smbus
#import time
#from time import sleep
#import sys

bus = smbus.SMBus(1)

busAddress = 0x71

displayDataAddressPtr = 0x00
systemSetupAddress = 0x20
keyDataAddressPtr = 0x40
INTflagAddressPtr = 0x60

# I2C Read
#read_byte(i2c_addr,force=None)
#read_byte_data(i2c_addr,register,force=None)
#read_block_data(i2c_addr,register,force=None)
#read_i2c_block_data(i2c_addr,register,length,force=None)
#read_word_data(i2c_addr,register,force=None)


value = bus.read_byte_data(busAddress, displayDataAddressPtr)
print("displayDataAddressPtr value= 0x%X" % (value))
#print("\n")

value = bus.read_byte_data(busAddress, systemSetupAddress)
print("systemSetupAddress: 0x%X" % (value))
#print("\n")

value = bus.read_byte_data(busAddress, keyDataAddressPtr)
print("keyDataAddressPtr: 0x%X" % (value))
#print("\n")

value = bus.read_byte_data(busAddress, INTflagAddressPtr)
print("INTflagAddressPtr: 0x%X" % (value))
#print("\n")



