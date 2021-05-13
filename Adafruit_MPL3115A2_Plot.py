# Plotting MPL3115A2 sensor data
import time
import datetime as dt

import board
import busio

import adafruit_mpl3115a2
import matplotlib.pyplot as plt

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize MPL3115A2
sensor = adafruit_mpl3115a2.MPL3115A2(i2c)
#sensor = adafruit_mpl3115a2.MPL3115A2(i2c, address=0x10)

# You can configure the pressure at sealevel to get better altitude estimates.
# This value has to be looked up from your local weather forecast or meteorlogical
# reports.  It will change day by day and even hour by hour with weather
# changes.  Remember altitude estimation from barometric pressure is not exact!
# Set this to a value in pascals:
sensor.sealevel_pressure = 102250

# Main loop to read the sensor values and print them every second.
#while True:
#    pressure = sensor.pressure
#    print('Pressure: {0:0.3f} pascals'.format(pressure))
#    altitude = sensor.altitude
#    print('Altitude: {0:0.1f} meters'.format(altitude))
#    temperature = sensor.temperature
#    tempF = temperature * 1.8 + 32.0
#    print('Temperature: {0:0.1f} degrees Celsius'.format(temperature))
#    print('   {0:0.1f} degress Fahrenheit'.format(tempF))
#    time.sleep(4.0)
#    print('')

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

# Sample temperature every second for 10 seconds
print('--- Start ---')
for t in range(0, 10):

    # Get sensor data
    # Seem to need to get all data (?)
    pressure = sensor.pressure
    altitude = sensor.altitude
    temp_c = round(sensor.temperature, 2)
#    temp_c = sensor.temperature
    
    # Add x and y to lists
    xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    ys.append(temp_c)

    # Wait 1 second before sampling temperature again
    time.sleep(1)

# Draw plot
ax.plot(xs, ys)

# Format plot
plt.xticks(rotation=45, ha='right')
plt.subplots_adjust(bottom=0.30)
plt.title('TMP102 Temperature over Time')
plt.ylabel('Temperature (deg C)')

# Draw graph (blocking!)
plt.show()

print('!!!')
