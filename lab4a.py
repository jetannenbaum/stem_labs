# Author: J.E. Tannenbaum
# Initial Release: 01/13/2022
# Using Pulse Width Modulation to control LED
from machine import Pin, PWM
from time import sleep

# Define the pwm for the led
led = PWM(Pin(17))

# Set up the list of frequencies
frequencyList = [1000, 500, 100, 50, 40, 30, 20, 10]

# run through the list
for frequency in frequencyList:
    
    # define the pwm frequency
    led.freq(frequency)
    print('Frequency: ' + str(frequency))

    # Loop from completely off to completely on
    for dutyCycle in range(65535):
        led.duty_u16(dutyCycle)
        sleep(0.0001)

    print('Full bright!')

    # Loop from completely on to completely off
    for dutyCycle in range(65535, 0, -1):
        led.duty_u16(dutyCycle)
        sleep(0.0001)

    print('Full off!')
