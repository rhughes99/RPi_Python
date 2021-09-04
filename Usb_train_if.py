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

# was it found?
if dev is None:
    raise ValueError('*** Device not found')

print('Device found')

# set active configuration. With no arguments, first configuration will be active one
dev.set_configuration()

# get an endpoint instance
cfg = dev.get_active_configuration()
intf = cfg[(0,0)]

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
print('Iterating over configurations and interfaces...')
for cfg in dev:
    sys.stdout.write(str(cfg.bConfigurationValue) + '\n')
    for intf in cfg:
        sys.stdout.write('\t' + \
                         str(intf.bInterfaceNumber) + \
                         ',' + \
                         str(intf.bAlternateSetting) + \
                         '\n')
        for ep in intf:
            sys.stdout.write('\t\t' + \
                             str(ep.bEndpointAddress) + \
                             '\n')


print('Sending ctrl_transfer...')
data = 0x00000000
dev.ctrl_transfer(0xF0, 0x40, 0, 0, data)

print('Sending write...')
data = 0x00000000000FFFFF
ep.write(data)



# bmRequestType =	USBmakebmRequestType(kUSBOut, kUSBVendor, kUSBDevice);
#reqType = 0xF0
#bReq = 0xF0			# SetIoPortsConfig
#wVal = 0			# unused
#wIndex = 0			# unused
# wLength	 = 4;						// 32bit int
# pData    = &portBits;

#device.ctrl_transfer(reqType, bReq, wVal, wIndex, data)

