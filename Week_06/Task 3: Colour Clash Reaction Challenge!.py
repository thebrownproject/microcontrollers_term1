# Imports
from machine import Pin, PWM, ADC
import time
import random
import os

# Hardware setup
leds = [
    Pin(0, Pin.OUT),
    Pin(1, Pin.OUT),
    Pin(2, Pin.OUT)
    ]
buttons = [
    Pin(10, Pin.IN, Pin.PULL_UP),
    Pin(11, Pin.IN, Pin.PULL_UP),
    Pin(12, Pin.IN, Pin.PULL_UP)
    ]
buzzer = PWM(Pin(7))

# Game state variables
round_no = 0
active_led = 0
player_selection = 0
player_name = ""

# Buzzer sound functions
def buzzer_start_game():
    buzzer.duty_u16(20000)  # Set duty cycle for sound output
    frequencies = [659, 659, 0, 659, 0, 523, 659, 0, 784, 0, 0, 0, 392, 0, 0, 0]
    for freq in frequencies:
        if freq == 0:
            buzzer.duty_u16(0)
        else:
            buzzer.freq(freq)  # Set frequency for buzzer
            buzzer.duty_u16(20000)
        time.sleep(0.15)  
    buzzer.duty_u16(0)
def buzzer_next_round():
    buzzer.duty_u16(20000)  # Set duty cycle for sound output
    frequencies = [300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900]
    for freq in frequencies:
        buzzer.freq(freq)  # Set frequency for buzzer
        time.sleep(0.05)
    buzzer.duty_u16(0)
def buzzer_win():
    buzzer.duty_u16(20000)
    frequencies = [(660,0.1),(660,0.1),(0,0.1),(660,0.1),(0,0.1),(510,0.1),(660,0.1),(770,0.1),(0,0.1),(380,0.1),
(0,0.1),(510,0.1),(0,0.1),(380,0.1),(320,0.1),(0,0.1)]
    for freq, times in frequencies:
        if freq == 0:
            time.sleep(times)
        else:
            buzzer.freq(freq)
            time.sleep(times)
    buzzer.duty_u16(0)
def buzzer_lose():
    buzzer.duty_u16(20000)
    frequencies = [400, 350, 300, 250, 200, 150, 100, 50]
    for freq in frequencies:
        buzzer.freq(freq)
        time.sleep(0.1)
    buzzer.duty_u16(0)

# Game logic / game state
def game_start():
    global player_name
    print("Welcome to Colour Clash Reaction Challenge!")
    buzzer_start_game()
    with open("scoreboard.txt", "r") as file:
        content = file.read()
        print(content)
    player_name = input("Enter your gamer tag: ")
    buzzer_next_round()
    light_flash()
# show current 5 top scores

# randon rgb shown
def light_flash():
    global active_led
    random_index = random.randint(0, 2)
    leds[random_index].on()
    time.sleep(1)
    leds[random_index].off()
    active_led = random_index
    player_turn()

def player_turn():
    global player_selection
    while True:
        for i in range(len(buttons)):
            if buttons[i].value() == 0:
                print(f"Button {i} pressed!")
                player_selection = i
                check_win()
                return

def check_win():
    global round_no, active_led, player_selection
    if active_led == player_selection:
        round_no += 1
        if round_no == 2:
            game_win()
            return
        print(f"Correct! Lets move to round {round_no + 1}")
        buzzer_next_round()
        time.sleep(.5)
        light_flash()
    else:
        print("Wrong! Game over!")
        buzzer_lose()
        game_restart()

def game_win():
    print("You have won the game champ!")
    buzzer_win()
    game_restart()
    file = open("scoreboard.txt", "a")
    file.write(f"{player_name} {round_no + 1}\n")
    file.close()

def game_restart():
    global round_no
    user_input = input("Do you want to play again? (yes or no): ")
    if user_input == "yes":
        round_no = 0
        buzzer_start_game()
        light_flash()
    elif user_input == "no":
        print("Thanks for playing, have a good one!")
        return
    else:
        print("Not a valid input, try again!")
        game_restart()

def show_leaderboard():
    try:
        with open("scoreboard.txt", "r") as file:
            lines = file.readlines()
            scores = []
            for line in lines:
                parts = line.strip().split()
                if len[parts] == 2 and parts[1].isdigit():
                    name = parts[0]
                    score = int(parts[1])
                    scores.append((name, score))

    except FileNotFoundError:
        print("No leaderboard data found!")
        
# Game entry point
game_start()

