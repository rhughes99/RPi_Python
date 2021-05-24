# Train Board
#  Uses gpiozero for input
#   and smbus (I2C) for output (relay control)
# First version used downstairs under the train table

import time
import smbus
import gpiozero

blueLED  = gpiozero.LED(4)
greenLED = gpiozero.LED(17)
redLED   = gpiozero.LED(18)

# RENAME: UNLOAD UNCOUPLE SWITCH
in1 = gpiozero.Button(19)
in2 = gpiozero.Button(16)
in3 = gpiozero.Button(13)

# Not connected
in4 = gpiozero.Button(12)
in5 = gpiozero.Button(6)
in6 = gpiozero.Button(5)

# All relay module address switches off
busAddress = 0x27
bus = smbus.SMBus(1)
relayCmd = bus.read_byte(busAddress)

# Turn LEDs off (outputs = 1)
blueLED.on()
greenLED.on()
redLED.on()

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

while True:
    try:
        # Active input = 0, not pressed
        if in1.is_pressed:
            print('IN 1 ON')
            relayCmd &= 0b11111110
            bus.write_byte(busAddress, relayCmd)
            blueLED.off()
        else:
            print('    IN 1 off')
            relayCmd |= 0b00000001
            bus.write_byte(busAddress, relayCmd)
            blueLED.on()

        if in2.is_pressed:
            print('IN 2 ON')
            relayCmd &= 0b11111101
            bus.write_byte(busAddress, relayCmd)
            greenLED.off()
        else:
            print('    IN 2 off')
            relayCmd |= 0b00000010
            bus.write_byte(busAddress, relayCmd)
            greenLED.on()

        if in3.is_pressed:
            print('IN 3 ON')
            relayCmd &= 0b11111011
            bus.write_byte(busAddress, relayCmd)
            redLED.off()
        else:
            print('    IN 3 off')
            relayCmd |= 0b00000100
            bus.write_byte(busAddress, relayCmd)
            redLED.on()

#        if in4.is_pressed:
#            print('IN 4 ON')
#            relayCmd &= 0b11110111
#            bus.write_byte(busAddress, relayCmd)
#        else:
#            print('    IN 4 off')
#            relayCmd |= 0b00001000
#            bus.write_byte(busAddress, relayCmd)

#        if in5.is_pressed:
#            print('IN 5 ON')
#            relayCmd &= 0b11101111
#            bus.write_byte(busAddress, relayCmd)
#        else:
#            print('    IN 5 off')
#            relayCmd |= 0b00010000
#            bus.write_byte(busAddress, relayCmd)

#        if in6.is_pressed:
#            print('IN 6 ON')
#            relayCmd &= 0b11011111
#            bus.write_byte(busAddress, relayCmd)
#        else:
#            print('    IN 6 off')
#            relayCmd |= 0b00100000
#            bus.write_byte(busAddress, relayCmd)

        time.sleep(1)
        print('')

    except KeyboardInterrupt as ki:
        bus.write_byte(busAddress, 0xFF)
        print('-------')
        print('Exiting...')
        break

