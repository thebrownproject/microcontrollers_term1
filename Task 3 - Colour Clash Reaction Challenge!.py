from machine import Pin, PWM, ADC
import time
import random

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

round_no = 0
active_led = 0
player_selection = 0

buzzer = PWM(Pin(7))

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
    frequencies = [500, 400, 300, 200]
    for freq in frequencies:
        buzzer.freq(freq)
        time.sleep(0.2)
    buzzer.duty_u16(0)

# randon rgb shown





# randon rgb shown
def light_flash():
    global active_led
    random_index = random.randint(0, 2)
    leds[random_index].on()
    time.sleep(1)
    leds[random_index].off()
    active_led = random_index
    return player_turn() # Return the status from player_turn


def player_turn():
    global player_selection
    print("Player turn: Press the button matching the LED!")
    while True:
        for i in range(len(buttons)):
            if buttons[i].value() == 0:
                # Basic debounce
                time.sleep(0.1) 
                if buttons[i].value() == 0: 
                    print(f"Button {i} pressed!")
                    player_selection = i
                    return check_win() # Return the status from check_win
        time.sleep(0.01) # Small delay to prevent busy-waiting

def check_win():
    global round_no, active_led, player_selection
    if active_led == player_selection:
        round_no += 1
        if round_no >= 3: # Win condition (e.g., 3 rounds)
            print(f"Correct! Round {round_no} complete.")
            print("YOU WIN! 🎉")
            buzzer_win()
            return 'win' # Signal win
        else:
            print(f"Correct! Round {round_no} complete. Next round!")
            buzzer_next_round()
            time.sleep(0.5)
            return 'continue' # Signal to continue game
    else:
        print(f"Incorrect! The active LED was {active_led}, you pressed {player_selection}.")
        print("GAME OVER! 😭")
        buzzer_lose()
        return 'lose' # Signal loss

def game_loop():
    global round_no
    round_no = 0 # Reset round number for new game
    print("\n--- NEW GAME ---")
    buzzer_start_game()
    time.sleep(1) # Pause before first flash

    while True:
        print(f"\n--- Round {round_no + 1} ---")
        status = light_flash() # This now returns 'continue', 'win', or 'lose'
        
        if status == 'continue':
            # The check_win function already handled the 'next round' sound and message
            continue 
        elif status == 'win':
            # Win message and sound handled in check_win
            time.sleep(2) # Pause after win
            break # Exit the inner loop to restart game
        elif status == 'lose':
            # Lose message and sound handled in check_win
            time.sleep(2) # Pause after loss
            break # Exit the inner loop to restart game

# Main execution - keeps restarting the game
while True:
    game_loop()
    print("Restarting game in 3 seconds...")
    time.sleep(3)
