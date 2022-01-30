# Author: J.E. Tannenbaum
# Initial Release: 01/29/2022
# Scrolling text on a I2C SSD1306 display
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time

i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)
 
yDir = 1 
xDir = 1
oled.text("Hello Esperanza", 0, 1)
oled.show()
for i in range(100):
    oled.scroll(xDir, yDir)
    oled.show()
    time.sleep(.05)
    if i > 49:
        yDir = -1
    if i % 14 == 0:
        xDir = 1
    elif i % 7 == 0:
        xDir = -1


