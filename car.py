from machine import Pin, PWM, UART
import utime
import time
from neopixel import NeoPixel

NUMBER_PIXELS = 2
LED_PIN = 18

#Define the pin as output
pin = Pin(LED_PIN, Pin.OUT)

# Define the NeoPixel Strip
strip = NeoPixel(pin, NUMBER_PIXELS)

# Color RGB values
red = (255, 0, 0)
yellow = (255, 150, 0)
green = (0, 255, 0)
black = (0, 0, 0)
startColors = (red, black, red, black, yellow, black, yellow, black, green, black, green, black)

def showColor(color):
    for i in range(NUMBER_PIXELS):
        strip[i] = color
    strip.write()

# Using Grove 5 Connector
TRIGGER_PIN = 6 # White Wire
ECHO_PIN = 26 # Yellow Wire

# Init HC-SR04P pins
trigger = Pin(TRIGGER_PIN, Pin.OUT) # send trigger out to sensor
echo = Pin(ECHO_PIN, Pin.IN) # get the delay interval back

def ping():
    trigger.low()
    utime.sleep_us(2) # Wait 2 microseconds low
    trigger.high()
    utime.sleep_us(5) # Stay high for 5 microseconds
    trigger.low()
    while echo.value() == 0:
        signaloff = utime.ticks_us()
    while echo.value() == 1:
        signalon = utime.ticks_us()
    timepassed = signalon - signaloff
    distance = (timepassed * 0.0343) / 2
    return distance * .254

BUZZER_PIN = 22
buzzer = PWM(Pin(BUZZER_PIN))

def playTone():
    buzzer.duty_u16(1000)
    buzzer.freq(150)

def stopTone():
    buzzer.duty_u16(0)
    
#define the UART
uart0 = UART(id=1, baudrate=9600, tx=Pin(4), rx=Pin(5))

# Get the data from the UART
def readUartBytes(uart):
    resp = b""
    while uart.any():
        resp = b"".join([resp, uart.read(1)])
    return resp.decode()

# Motor definitions
FULL_POWER_LEVEL = 65024
RIGHT_FORWARD_PIN = 11
RIGHT_REVERSE_PIN = 10
LEFT_FORWARD_PIN = 9
LEFT_REVERSE_PIN = 8

right_forward = PWM(Pin(RIGHT_FORWARD_PIN))
right_reverse = PWM(Pin(RIGHT_REVERSE_PIN))
left_forward = PWM(Pin(LEFT_FORWARD_PIN))
left_reverse = PWM(Pin(LEFT_REVERSE_PIN))

def forward():
    right_reverse.duty_u16(0)
    left_reverse.duty_u16(0)
    right_forward.duty_u16(FULL_POWER_LEVEL)
    left_forward.duty_u16(FULL_POWER_LEVEL)

def forwardSlow():
    right_reverse.duty_u16(0)
    left_reverse.duty_u16(0)
    right_forward.duty_u16(FULL_POWER_LEVEL // 2)
    left_forward.duty_u16(FULL_POWER_LEVEL // 2)

def reverse():
    right_forward.duty_u16(0)
    left_forward.duty_u16(0)
    right_reverse.duty_u16(FULL_POWER_LEVEL)
    left_reverse.duty_u16(FULL_POWER_LEVEL)
    
def reverseSlow():
    right_forward.duty_u16(0)
    left_forward.duty_u16(0)
    right_reverse.duty_u16(FULL_POWER_LEVEL // 2)
    left_reverse.duty_u16(FULL_POWER_LEVEL // 2)

def left():
    left_forward.duty_u16(0)
    right_reverse.duty_u16(0)
    left_reverse.duty_u16(FULL_POWER_LEVEL)    
    right_forward.duty_u16(FULL_POWER_LEVEL)
    
def right():
    right_forward.duty_u16(0)
    left_reverse.duty_u16(0)
    right_reverse.duty_u16(FULL_POWER_LEVEL)    
    left_forward.duty_u16(FULL_POWER_LEVEL)
    
def stop():
    right_forward.duty_u16(0)
    right_reverse.duty_u16(0)
    left_forward.duty_u16(0)
    left_reverse.duty_u16(0)

def reverseAndTurn():
    utime.sleep(.5)
    reverseSlow()
    utime.sleep(1.5)
    left_reverse.duty_u16(0)
    left_forward.duty_u16(FULL_POWER_LEVEL // 2)
    utime.sleep(.75)
    stop()
    utime.sleep(.25)
    stopTone()

for color in startColors:
    showColor(color)
    utime.sleep(.5)

forward()      # Assume the way ahead is clear
color = green
while True:
    dir = readUartBytes(uart0) # read from the UART
    if dir == 'h':
        stop()
        color = red
    elif dir == 'f':
        forward()
        color = green
    elif dir == 'l':
        left()
        color = green
    elif dir == 'r':
        right()
        color = green
    distance = ping()  # Check the distance
    if distance < 5 or dir == 's':   # Obstruction ahead, slow down
        forwardSlow()
        color = yellow
    if distance < 2.5: # Obstruction too close, stop, and play tone
        stop()
        color = red
        playTone()
    showColor(color)
    if distance < 2.5:  # If we were too close, back up and turn
        reverseAndTurn()
        forward()
        color = green
