# Plotting MPL3115A2 sensor data
import time
import datetime as dt

import board
import busio

import adafruit_mpl3115a2
from adafruit_ht16k33 import segments

import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize I2C components
sensor = adafruit_mpl3115a2.MPL3115A2(i2c)
display = segments.Seg7x4(i2c)
display.fill(0)

# Create figure for plotting
fig = plt.figure()
xTimeStamp = []

aTemp = fig.add_subplot(2, 1, 1)
yTemp = []

aPress = fig.add_subplot(2, 1, 2)
yPress = []

# Called periodically from FuncAnimation
def animate(i, xTimeStamp, yTemp, yPress):
    # Get sensor data
    # Seem to need to get extra data (?) to get temperature
    pressure = sensor.pressure
    pressureInch = pressure * 3.10552 * 0.0001
    pressureInch = round(pressureInch * 100) / 100 - 0.9
#    altitude = sensor.altitude
    tempC = sensor.temperature
    tempF = tempC * 1.8 + 32.0
    tempF = round(tempF * 10) / 10

    # Add x and y to lists
#    xTimeStamp.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    xTimeStamp.append(dt.datetime.now().strftime('%M:%S'))
    yTemp.append(tempF)
    yPress.append(pressureInch)

    display.fill(0)
    display.print(round(tempF))

    # Limit x and y lists to 20 items
    xTimeStamp = xTimeStamp[-20:]
    yTemp = yTemp[-20:]
    yPress = yPress[-20:]

    # Draw x and y lists
    aTemp.clear()
    aTemp.plot(xTimeStamp, yTemp)
    aPress.clear()
    aPress.plot(xTimeStamp, yPress)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
#    plt.title('title')
#    plt.ylabel('ylabel')


print('--- Start ---')
# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xTimeStamp, yTemp, yPress), interval=2000)
plt.show()

print('Program ended...')

