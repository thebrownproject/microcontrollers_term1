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
    time.sleep(.4)
    
    while True:
        melody_level_up()
        light_flash()
        if not player_turn():
            break
        # Success - proceed to next round
        round_no += 1
        print(f"Round {round_no} passed! Let's move to round {round_no + 1}")
        time.sleep(.5)
    
    print(f"Well done {player_name}, you have scored {round_no}!")
    with open("scoreboard.txt", "a") as file:
        file.write(f"{player_name} {round_no}\n")
        file.close()
    show_leaderboard()
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
    
    current_index = 0
    while current_index < expected_presses:
        for i in range(len(buttons)):
            if buttons[i].value() == 0:  # Button pressed
                print(f"Button {i + 1} pressed!")
                
                # Play sound for the button pressed
                game_tone(game_tones[i])
                
                # Visual feedback
                leds[i].on()
                time.sleep(0.2)
                leds[i].off()
                
                # Check if this button press matches the expected LED
                if i != active_leds[current_index]:
                    print("Wrong! Game over!")
                    melody_game_over()
                    return False
                
                player_selection.append(i)
                current_index += 1
                
                while buttons[i].value() == 0:
                    time.sleep(0.1)
                
                time.sleep(0.1)
                break
    return True

def show_leaderboard():
    try:
        with open("scoreboard.txt", "r") as file:
            lines = file.readlines()
            scores = []
            for line in lines:
                parts = line.strip().split()
                if len(parts) == 2 and parts[1].isdigit():
                    name = parts[0]
                    score = int(parts[1])
                    scores.append((name, score))
            
            top_scores = sorted(scores, key=lambda x: x[1], reverse=True)[:5]

            print("\n🏆 TOP 5 SCORES 🏆")
            for i, (name, score) in enumerate(top_scores, 1):
                print(f"{i}. {name} - {score}")

    except FileNotFoundError:
        print("No leaderboard data found!")

# Game entry point
game_start()