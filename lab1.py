# Author: J.E. Tannenbaum
# Initial Release: 01/13/2022
# Blink an Led
from machine import Pin
from time import sleep

# Define the pin for the onboard led
led1 = Pin(25, Pin.OUT)

# make sure it is off
led1.low()

# Toggle it on for 1 second, then off for one second forever
while True:
	led1.toggle()
	sleep(1)