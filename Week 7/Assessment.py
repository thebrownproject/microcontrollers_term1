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
active_leds = []
player_selection = []
player_name = ""

# Buzzer sound functions
def play_tone(frequency, duration):
    buzzer.freq(frequency)  # Set frequency for buzzer
    time.sleep(duration / 1000)  # Convert milliseconds to seconds

def melody_game_start():
    buzzer.duty_u16(20000)  # Set duty cycle for sound output
    notes = [
        (392, 200),  # G
        (494, 200),  # B
        (587, 200),  # D
        (784, 400)   # G (higher octave)
    ]
    for tone, duration in notes:
        play_tone(tone, duration)
        time.sleep(0.05)  # Short pause between notes
    buzzer.duty_u16(0)  # Turn off buzzer

def melody_level_up():
    buzzer.duty_u16(20000)  # Set duty cycle for sound output
    for tone in [329, 392, 659, 523, 587, 784]:
        play_tone(tone, 150)
        time.sleep(0.15)
    buzzer.duty_u16(0)

def melody_game_over():
    buzzer.duty_u16(20000)  # Set duty cycle for sound output
    play_tone(622, 300)
    time.sleep(0.3)
    play_tone(587, 300)
    time.sleep(0.3)
    play_tone(554, 300)
    time.sleep(0.3)
    for _ in range(10):
        for pitch in range(-10, 11):
            play_tone(523 + pitch, 5)
    time.sleep(0.5)
    buzzer.duty_u16(0)

# game logic / game state
def game_start():
    global player_name
    print("Welcome to Memory Challenge!")
    melody_game_start()
    player_name = input("Please enter your player name: ")
    time.sleep(.5)
    print(f"Okay {player_name}, let's start the game!")

    while True:
        melody_level_up()
        light_flash()
        print(f"Well done {player_name}, you have scored {round_no + 1}!")
        user_input = input("Do you want to play again? (type yes): ")
        if user_input.lower() == "yes":
            global round_no
            round_no = 0
        else:
            print("Thanks for playing!")
            melody_game_over()
            break


# Game entry point
game_start()