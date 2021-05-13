from gpiozero import LED
from time import sleep

#led = LED(3)     # SCL
#led = LED(14)    # TxD
#led = LED(15)    # RxD
led = LED(18)
delay = 1.0

while True:
  led.on()
  sleep(delay)
  led.off()
  sleep(delay/2)

#led.off()
