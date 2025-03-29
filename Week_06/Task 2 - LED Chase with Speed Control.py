from machine import PWM, Pin, ADC
import time


leds = [
    Pin(3, Pin.OUT),
    Pin(4, Pin.OUT),
    Pin(5, Pin.OUT),
    Pin(6, Pin.OUT),
    Pin(7, Pin.OUT)
]

adc = ADC(Pin(26))

def get_delay():
    """Reads potentiometer value and converts it to delay time."""
    raw_value = adc.read_u16()
    delay = 0.05 + (raw_value / 65535) * 0.25  # Range: 0.05s - 0.25s
    return delay

while True:

    
    for led in leds:
        led.value(1)
        time.sleep(get_delay())
        led.value(0)
        
    for led in reversed(leds):
        led.value(1)
        time.sleep(get_delay())
        led.value(0)




# adc = ADC(Pin(26))        # create an ADC object acting on a pin
# led = PWM(Pin(3))
# led.freq(1000)

# while True:
#    val = adc.read_u16()  # read a raw analog value in the range 0-65535
#    print(val)
    
#    led.duty_u16(val)
#    time.sleep(0.20)