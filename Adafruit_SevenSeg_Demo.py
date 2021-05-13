# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Basic example of setting digits on a LED segment display.
# This example and library is meant to work with Adafruit CircuitPython API.
# Author: Tony DiCola
# License: Public Domain

import time

# Import all board pins.
import board
import busio

# Import the HT16K33 LED segment module.
from adafruit_ht16k33 import segments

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# Create the LED segment class.
# This creates a 7 segment 4 character display:
display = segments.Seg7x4(i2c)
# Or this creates a 14 segment alphanumeric 4 character display:
# display = segments.Seg14x4(i2c)
# Or this creates a big 7 segment 4 character display
# display = segments.BigSeg7x4(i2c)
# Finally you can optionally specify a custom I2C address of the HT16k33 like:
# display = segments.Seg7x4(i2c, address=0x70)

# Clear the display.
display.fill(0)

# Can just print a number
#display.print(42)
display.print("42.1")
time.sleep(2)

# Or, can print a hexadecimal value
display.print_hex(0xFA23)
time.sleep(2)

# Or, print the time
display.print("12:30")
time.sleep(2)

display.colon = False

# Or, can set indivdual digits / characters
# Set the first character to '1':
#display[0] = "6"
display.fill(0)
# Set the second character to '2':
display[1] = "0"
# Set the third character to 'A':
display[2] = "A"
# Set the forth character to 'B':
display[3] = "C"
time.sleep(2)

# Or, can even set the segments to make up characters
if isinstance(display, segments.Seg7x4):
    # 7-segment raw digits
    print("  7-segment raw digits")
    display.set_digit_raw(0, 0xFF)
    display.set_digit_raw(1, 0b11111111)
    display.set_digit_raw(2, 0x79)
    display.set_digit_raw(3, 0b01111001)
else:
    # 14-segment raw digits
    print("  14-segment raw digits")
    display.set_digit_raw(0, 0x2D3F)
    display.set_digit_raw(1, 0b0010110100111111)
    display.set_digit_raw(2, (0b00101101, 0b00111111))
    display.set_digit_raw(3, [0x2D, 0x3F])
time.sleep(4)

# Show a looping marquee
display.marquee("A B C D...   ", 0.4)
