import smbus
from time import sleep
#import sys

bus = smbus.SMBus(1)

# All address switches off
busAddress = 0x27

#read_byte(i2c_addr, force=None)
#write_byte(i2c_addr, data, force=None)

value = bus.read_byte(busAddress)
print("Start: value= 0x%X" % (value))

#bus.write_byte(busAddress, 0xFE)
#value = bus.read_byte(busAddress)
#print("  value= 0x%X" % (value))

bus.write_byte(busAddress, 0xFF)
sleep(1)

#for wValue in range(0xFF, 0x00, -1):
#    bus.write_byte(busAddress, wValue)
    
#    value = bus.read_byte(busAddress)
#    print("value= 0x%X" % (value))
#    sleep(1)

bus.write_byte(busAddress, 0xFE)
sleep(2)
bus.write_byte(busAddress, 0xFC)
sleep(2)
bus.write_byte(busAddress, 0xF8)
sleep(2)
bus.write_byte(busAddress, 0xF0)
sleep(2)
bus.write_byte(busAddress, 0xE0)
sleep(2)
bus.write_byte(busAddress, 0xC0)
sleep(2)
bus.write_byte(busAddress, 0x80)
sleep(2)
bus.write_byte(busAddress, 0x00)
sleep(4)

bus.write_byte(busAddress, 0xFF)




