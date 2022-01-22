# Author: J.E. Tannenbaum
# Initial Release: 01/17/2022
# Playing with a neopixel bar

import time
# We are using https://github.com/blaz-r/pi_pico_neopixel
from neopixel import Neopixel

NUMBER_PIXELS = 8
STATE_MACHINE = 0
LED_PIN = 0

# We are using the GRB variety, not RGB
strip = Neopixel(NUMBER_PIXELS, STATE_MACHINE, LED_PIN, "GRB")
# set 100% brightness
strip.brightness(100)
delay = .1

# set the colors from https://www.rapidtables.com/web/color/RGB_Color.html
white = (255, 255, 255)
red = (255, 0, 0)
orange = (255, 165, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
indigo = (75, 0, 130)
violet = (148, 0,211)
black = (0, 0, 0)
colors = (black, white, red, orange, yellow, green, blue, indigo, violet, black)

while True:
    for color in colors:
        for i in range(NUMBER_PIXELS):
            strip.set_pixel(i, color)
            strip.show()
            time.sleep(delay)
        