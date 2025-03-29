from machine import Pin
from machine import ADC
from machine import PWM
import time


# 1. Connect an LED to the appropriate GPIO on the Raspberry Pi Pico 
# 2. Connect a potentiometer to the appropriate GPIO(ADC)
# 3. Use ADC to read the Analog value from the potentiometer.
# 4. Use PWM to control the LED’s brightness based on the potentiometer input.
# 5. Add a short delay in the loop to smooth the brightness transition.

adc = ADC(Pin(26))        # create an ADC object acting on a pin
led = PWM(Pin(3))
led.freq(1000)

while True:
    val = adc.read_u16()  # read a raw analog value in the range 0-65535
    print(val)
    
    led.duty_u16(val)
    time.sleep(0.20)