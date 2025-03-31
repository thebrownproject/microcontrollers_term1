from machine import Pin, PWM
import time
import random

# Hardware setup
leds = [
    Pin(0, Pin.OUT),
    Pin(1, Pin.OUT),
    Pin(2, Pin.OUT),
    Pin(3, Pin.OUT)
]

buttons = [
    Pin(15, Pin.IN, Pin.PULL_UP),
    Pin(14, Pin.IN, Pin.PULL_UP),
    Pin(13, Pin.IN, Pin.PULL_UP),
    Pin(12, Pin.IN, Pin.PULL_UP)
]

buzzer = PWM(Pin(11))

# Game state variables
round_no = 0
active_led = []
player_selection = []
player_name = ""



def play_level_up():
    buzzer.duty_u16(20000)  # Set duty cycle for sound output
    for tone in [329, 392, 659, 523, 587, 784]:
        play_tone(tone, 150)
        time.sleep(0.15)
    buzzer.duty_u16(0)

play_level_up()