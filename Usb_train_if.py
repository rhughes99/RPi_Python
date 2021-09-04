import usb.core
import usb.util
import sys
#import usb.backend.libusb1

VENDOR_ID =  0x0ABF
PRODUCT_ID = 0x03ED

# from Programming with PyUSB 1.0
# https://github.com/pyusb/pyusb/blob/master/docs/tutorial.rst#id9

# find our device
dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

# Was it found?
if dev is None:
    raise ValueError('*** Device not found')

print('Device found')

# Show all configurations
#for cfg in dev:
#    sys.stdout.write(str(cfg.bConfigurationValue) + '\n')
#print('\n\n')

# Set active configuration.
# With no arguments, first configuration will be active one
dev.set_configuration()

# get an endpoint instance
print('Getting cfg and intf...')
cfg = dev.get_active_configuration()
#print(cfg)
print('\n')
intf = cfg[(0,0)]
#print(intf)

# get endpoint instance
ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)

assert ep is not None


# iterate over a configuration to access interfaces, 
#  and iterate over interfaces to access endpoints
#print('Iterating over configurations and interfaces...')
#for cfg in dev:
#    sys.stdout.write(str(cfg.bConfigurationValue) + '\n')
#    for intf in cfg:
#        sys.stdout.write('\t' + \
#                         str(intf.bInterfaceNumber) + \
#                         ',' + \
#                         str(intf.bAlternateSetting) + \
#                         '\n')
#        for ep in intf:
#            sys.stdout.write('\t\t' + \
#                             str(ep.bEndpointAddress) + \
#                             '\n')


print('Sending ctrl_transfer...')
data = b'0x00000000'
dev.ctrl_transfer(0x40, 0xF0, 0, 0, data)


print('Sending write to:')
print(ep)
#data = b'0x00000000000FFFFF'
data = b'0x0000000000000000'
#data = 'asdf'
#ep.write(data)

#dev.write(0x02, data)
dev.write(0x03, data)



# bmRequestType =	USBmakebmRequestType(kUSBOut, kUSBVendor, kUSBDevice);
#reqType = 0xF0
#bReq = 0xF0			# SetIoPortsConfig
#wVal = 0			# unused
#wIndex = 0			# unused
# wLength	 = 4;						// 32bit int
# pData    = &portBits;

#device.ctrl_transfer(reqType, bReq, wVal, wIndex, data)

