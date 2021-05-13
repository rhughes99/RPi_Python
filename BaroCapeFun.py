# Playing around with Barometer Cape
#  MPL3115A2 barometric pressure sensor
#  7-segment HT16K33

import time

# Import all board pins.
import board
import busio

# Import the HT16K33 LED segment module.
from adafruit_ht16k33 import segments
import adafruit_mpl3115a2

# Create I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# Create the LED segment class & clear display
display = segments.Seg7x4(i2c)
display.fill(0)
#display.print("42.1")

# Initialize the MPL3115A2.
sensor = adafruit_mpl3115a2.MPL3115A2(i2c)

# You can configure the pressure at sealevel to get better altitude estimates.
# This value has to be looked up from your local weather forecast or meteorlogical
# reports.  It will change day by day and even hour by hour with weather
# changes.  Remember altitude estimation from barometric pressure is not exact!
# Set this to a value in pascals:
#sensor.sealevel_pressure = 102250
sensor.sealevel_pressure = 101325

# Main loop to read the sensor values and print them every second.
while True:
    pressure = sensor.pressure
    pressureInch = pressure * 3.10552 * 0.0001
    print('Pressure: {0:0.3f} pascals'.format(pressure))
    print('   {0:0.1f} inches'.format(pressureInch))
    altitude = sensor.altitude
    print('Altitude: {0:0.1f} meters'.format(altitude))
    temperature = sensor.temperature
    tempF = temperature * 1.8 + 32.0
    print('Temperature: {0:0.1f} degrees Celsius'.format(temperature))
    print('   {0:0.1f} degress Fahrenheit'.format(tempF))
    time.sleep(4.0)
    print('')


