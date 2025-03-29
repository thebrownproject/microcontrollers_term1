from machine import Pin, PWM, ADC
import time
import random

leds = [
    Pin(0, Pin.OUT),
    Pin(1, Pin.OUT),
    Pin(2, Pin.OUT)
    ]

for led in leds:
    led.off()