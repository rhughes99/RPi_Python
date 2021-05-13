from gpiozero import LED, Button

#led = LED(18)
led = LED(19, active_high=False)
button = Button(4)

#while True:
#    print("Top of while")
#    if button.is_pressed:
#        led.on()
#    else:
#        led.off()


#while True:
#    print("Step 1")
#    button.wait_for_press()
#    led.on()
#    print("Step 2")
#    button.wait_for_release()
#    led.off()


button.when_pressed  = led.on
#button.when_pressed  = led.blink
print("Step 1")
button.when_released = led.off
print("Step 2")
