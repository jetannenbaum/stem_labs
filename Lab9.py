# Author: J.E. Tannenbaum
# Initial Release: 01/29/2022
# Drawing lines on a I2C SSD1306 display
from machine import Pin, I2C, ADC
from ssd1306 import SSD1306_I2C
import time

# Takes an input number value and a range between high-and-low and returns it scaled to the new range
# This is similar to the Arduino map() function
def scaled(value, istart, istop, ostart, ostop):
  return int(ostart + (ostop - ostart) * ((int(value) - istart) / (istop - istart)))

i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

# Turn all pixels off
oled.fill(0)
oled.show()

# Provide info to user
oled.text('Line Drawing', 0, 0, 1)
oled.text('Hit the reset', 0, 20, 1)
oled.text('button to clear', 0, 30, 1)
oled.text('the screen', 0, 40, 1)
oled.show()

# Define the pin for the reset button
resetButton = Pin(16, Pin.IN, Pin.PULL_UP)

# Wait unti the user hits the button to clear the screen and start drawing
#while resetButton.value() != 1:
while resetButton.value():
    time.sleep(.25)
    
oled.fill(0)
oled.show()

# Define the Horizontal and Vertical inputs from the Rheostats
vert = ADC(26)
horiz = ADC(27)

# Calculate where to start the line
x = newX = scaled(vert.read_u16(), 0, 65535, 0, 127)
y = newY = scaled(horiz.read_u16(), 0, 65535, 0, 63)

# Loop forever
# Draw the line, look for a reset to clear the screen, and get the new end points for the line
while True:
    oled.line(x, y, newX, newY, 1)
    x = newX
    y = newY
    if resetButton.value() != 1:
        oled.fill(0)
    oled.show()
    time.sleep(.2)
    newX = 127 - scaled(vert.read_u16(), 0, 65535, 0, 127)
    newY = scaled(horiz.read_u16(), 0, 65535, 0, 63)
