from machine import Pin, ADC
from time import sleep

potentiometer = ADC(Pin(26))

while True:
    print(potentiometer.read_u16())
    sleep(0.05)