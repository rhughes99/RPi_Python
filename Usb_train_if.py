import os
#os.environ['PYUSB_DEBUG'] = 'debug' # uncomment for verbose pyusb output
import sys
import platform
from time import sleep

import usb.core
import usb.backend.libusb1
import usb.util

VENDOR_ID =  0x0ABF
PRODUCT_ID = 0x03ED

def write_to_device(dev, msg_str):
    print("Writing command: {}".format(msg_str))
    # message structure:
    #   message is an ASCII string containing the command
    #   8 bytes in lenth
    #   0th byte must always be 0x01
    #   bytes 1 to 7 are ASCII character values representing the command
    #   remainder of message is padded to character code 0 (null)
    byte_str = chr(0x01) + msg_str + chr(0) * max(7 - len(msg_str), 0)

    num_bytes_written = 0

    try:
        num_bytes_written = dev.write(0x01, byte_str)
    except usb.core.USBError as e:
        print (e.args)

    return num_bytes_written

def read_from_device(dev, timeout):
    try:
        data = dev.read(0x81, 64, timeout)
    except usb.core.USBError as e:
        print ("Error reading response: {}".format(e.args))
        return None

    byte_str = ''.join(chr(n) for n in data[1:])	# construct a string from read values, 
    												# starting from 2nd byte
    result_str = byte_str.split('\x00',1)[0]		# remove trailing null '\x00' chars

    if len(result_str) == 0:
        return None

    return result_str


was_kernel_driver_active = False
device = None

device = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

# if OS kernel already claimed device
#if device.is_kernel_driver_active(0) is True:
#    # tell kernel to detach
#    device.detach_kernel_driver(0)
#    was_kernel_driver_active = True

if device is None:
    raise ValueError('Device not found. Please ensure it is connected.')
    sys.exit(1)

#device.reset()

# Set active configuration. With no arguments, first configuration will be active one
#device.set_configuration()

# Claim interface 0
#usb.util.claim_interface(device, 0)



# bmRequestType =	USBmakebmRequestType(kUSBOut, kUSBVendor, kUSBDevice);
reqType = 0xF0
bReq = 0xF0			# SetIoPortsConfig
wVal = 0			# unused
wIndex = 0			# unused
# wLength	 = 4;						// 32bit int
# pData    = &portBits;

#device.ctrl_transfer(reqType, bReq, wVal, wIndex, data)
device.ctrl_transfer(reqType, bReq, wVal, wIndex, 0x0FFF)



# Write commands
# bytes_written = write_to_device(device, 'SK0')	# set relay 0
# bytes_written = write_to_device(device, 'RK0')	# reset relay 0

print("Write #1")
bytes_written = write_to_device(device, 'SK0')
sleep(2)

print("Write #2")
bytes_written = write_to_device(device, 'SK0')
sleep(2)


# Read
bytes_written = write_to_device(device, 'RPA')	# request value of PORT A in binary 
data = read_from_device(device, 200)			# read from device 
												# with a 200 millisecond timeout

if data != None:
    print("Received string: {}".format(data))
    print("Received data as int: {}".format(int(data)))

usb.util.release_interface(device, 0)

# Reattach kernel driver if we previously detached it
if was_kernel_driver_active == True:
    device.attach_kernel_driver(0)
