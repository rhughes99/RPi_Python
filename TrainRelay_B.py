# Train input and relay control
#  Uses gpiozero for input
#   and smbus (I2C) for output (relay control)

import time
import smbus
import gpiozero

led = gpiozero.LED(16)
in1 = gpiozero.Button(20)
in2 = gpiozero.Button(21)

# All relay module address switches off
busAddress = 0x27
bus = smbus.SMBus(1)
relayCmd = bus.read_byte(busAddress)
print("Relay Module Start: 0x%X" % (relayCmd))

while True:
    try:
        # LED on when output = 0
        led.on()
#        print('LED Off')
        time.sleep(1)
        
        led.off()
#        print('LED On')
        time.sleep(2)
        
        # Active input = 0, non pressed
        if in1.is_pressed:
#            print('Pin 1 ON')
            relayCmd &= 0b11111110
            bus.write_byte(busAddress, relayCmd)
        else:
#            print('Pin 1 off')
            relayCmd |= 0b00000001
            bus.write_byte(busAddress, relayCmd)
        
        if in2.is_pressed:
 #           print('Pin 2 ON')
            relayCmd &= 0b11111101
            bus.write_byte(busAddress, relayCmd)
        else:
 #           print('Pin 2 off')
            relayCmd |= 0b00000010
            bus.write_byte(busAddress, relayCmd)
        
#        time.sleep(1)
#        print('')
    
    except KeyboardInterrupt as ki:
        bus.write_byte(busAddress, 0xFF)
        led.on()
        print('-------')
        print('Exiting...')
        break

