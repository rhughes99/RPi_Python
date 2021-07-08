# Train Board
#  Uses gpiozero for input
#   and smbus (I2C) for output (relay control)
# For Everett

import time
import random
import smbus
import gpiozero

def playWithLights():
    dice = random.randint(1, 6)
    print(dice)

    for x in range(dice):
        rCmd = 0b11111111
        bus.write_byte(busAddress, rCmd)
        time.sleep(1)

        rCmd = 0b11110000
        bus.write_byte(busAddress, rCmd)
        time.sleep(1)

    bus.write_byte(busAddress, relayCmd)


blueLED  = gpiozero.LED(4)
greenLED = gpiozero.LED(17)
redLED   = gpiozero.LED(18)

# Inputs
UncoupleButton = gpiozero.Button(19)
UnloadButton   = gpiozero.Button(16)
Switch         = gpiozero.Button(13)

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

# Set starting "previous" states of switches
# 1 == is_pressed
previousUncouple = 0
previousUnload = 0

# Need to handle Switch differently because of two stable states
if Switch.is_pressed:
    relayCmd &= 0b11111011
    relayCmd |= 0b00001000
    bus.write_byte(busAddress, relayCmd)
    redLED.off()
    previousSwitch = 1
else:
    relayCmd |= 0b00000100
    relayCmd &= 0b11110111
    bus.write_byte(busAddress, relayCmd)
    redLED.on()
    previousSwitch = 0

garage = 0
station = 0
lightCnt = 0

while True:
    try:
        # Active input = 0, not pressed
        # garage and station are push-on, puch-off
        if UncoupleButton.is_pressed and previousUncouple == 0:
            previousUncouple = 1
            if garage == 0:
                relayCmd &= 0b11111110
                blueLED.off()
                garage = 1
            else:
                relayCmd |= 0b00000001
                blueLED.on()
                garage = 0

            bus.write_byte(busAddress, relayCmd)

        elif not(UncoupleButton.is_pressed) and previousUncouple == 1:
            previousUncouple = 0


        if UnloadButton.is_pressed and previousUnload == 0:
            previousUnload = 1
            if station == 0:
                relayCmd &= 0b11111101
                greenLED.off()
                station = 1
            else:
                relayCmd |= 0b00000010
                greenLED.on()
                station = 0

            bus.write_byte(busAddress, relayCmd)

        elif not(UnloadButton.is_pressed) and previousUnload == 1:
            previousUnload = 0


        if Switch.is_pressed and previousSwitch == 0:
#            print('Switch out: Red')
            relayCmd &= 0b11111011
            relayCmd |= 0b00001000
            bus.write_byte(busAddress, relayCmd)
            redLED.off()
            previousSwitch = 1

        elif not(Switch.is_pressed) and previousSwitch == 1:
            relayCmd |= 0b00000100
            relayCmd &= 0b11110111
            bus.write_byte(busAddress, relayCmd)
            redLED.on()
            previousSwitch = 0

        lightCnt = lightCnt + 1
        if lightCnt == 300:
            lightCnt = 0
            playWithLights()

        time.sleep(0.20)

    except KeyboardInterrupt as ki:
        bus.write_byte(busAddress, 0xFF)
        print('-------')
        print('Exiting...')
        break
