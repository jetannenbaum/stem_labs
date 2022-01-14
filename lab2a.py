# Author: J.E. Tannenbaum
# Initial Release: 01/13/2022
# Alternating blinking leds
from machine import Pin
from time import sleep

# Define the pin for each led
led1 = Pin(16, Pin.OUT)
led2 = Pin(17, Pin.OUT)

# make sure one is off and one is on
led1.low()
led2.high()

# wait a second before the endless loop
sleep(1)

# Toggle on for 1 second, then off for one second forever
while True:
	led1.toggle()
	led2.toggle()
	sleep(1)
