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
game_tones = [196, 261, 329, 784]

def game_tone(tone):
    buzzer.duty_u16(20000)  # Set duty cycle for sound output
    buzzer.freq(tone)  # Set frequency for buzzer
    time.sleep(0.2)  # Duration of the tone
    buzzer.duty_u16(0)  # Turn off buzzer

def play_tone(frequency, duration):
    buzzer.freq(frequency)  # Set frequency for buzzer
    time.sleep(duration / 1000)  # Convert milliseconds to seconds

def melody_game_start():
    notes = [
        (392, 200),  # G
        (494, 200),  # B
        (587, 200),  # D
        (784, 400)   # G (higher octave)
    ]
    for tone, duration in notes:
        buzzer.duty_u16(20000)  # Set duty cycle for sound output
        play_tone(tone, duration)
        buzzer.duty_u16(0)  # Turn off buzzer
        time.sleep(0.05)  # Short pause between notes

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
    global player_name, round_no
    melody_game_start()
    print("Welcome to Memory Challenge!")
    player_name = input("Please enter your player name: ")
    time.sleep(.5)
    print(f"Okay {player_name}, let's start the game!")
    time.sleep(1)  # Delay after game start message
    
    while True:
        melody_level_up()
        time.sleep(1)  # Delay AFTER the level-up tune and BEFORE the buttons light up
        light_flash()
        player_turn()
        if not check_win():
            break
    
    print(f"Well done {player_name}, you have scored {round_no + 1}!")
    user_input = input("Do you want to play again? (type yes): ")
    if user_input.lower() == "yes":
        round_no = 0
        active_leds.clear()
        player_selection.clear()
        game_start()
    else:
        print("Thanks for playing!")

# Function to flash LEDs in a sequence
def light_flash():
    global round_no
    random_index = random.randint(0, 3)
    active_leds.append(random_index)
    for led in active_leds:
        leds[led].on()
        game_tone(game_tones[led])
        time.sleep(0.5)
        leds[led].off()
        time.sleep(0.5)

# Function to check button presses
def player_turn():
    global player_selection
    player_selection = []
    expected_presses = len(active_leds)

    while len(player_selection) < expected_presses:
        for i in range(len(buttons)):
            if buttons[i].value() == 0: # Button pressed
                print(f"Button {i} pressed!")
                player_selection.append(i)

                # Play sound for the button pressed
                game_tone(game_tones[i])
                
                # Visual feedback
                leds[i].on()
                time.sleep(0.2)
                leds[i].off()

                while buttons[i].value() == 0:
                    time.sleep(0.1)
                
                time.sleep(0.1)
                break
    return

# Function to check if the player has won the round
def check_win():
    global round_no, active_leds, player_selection
    if active_leds == player_selection:
        round_no += 1
        print(f"Correct! Let's move to round {round_no + 1}")
        time.sleep(.5)
        return True
    else:
        print("Wrong! Game over!")
        melody_game_over()
        return False
    
# Game entry point
game_start()