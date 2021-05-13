import board
import digitalio
import busio

# From Adafruit Learning website
# 10/20/2019

print("Hello blinka!")

# Try to create a Digital input
pin = digitalio.DigitalInOut(board.D4)
print("Digital IO ok")

# Try to create an I2C device
i2c = busio.I2C(board.SCL, board.SDA)
print("I2C ok")

# Try to create an SPI device