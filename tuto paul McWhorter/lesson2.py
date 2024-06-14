''' Lesson 2
'''
from machine import Pin
from time import sleep
redLED = Pin(15, Pin.OUT)
while (True):
    try:
        redLED.value(0)
        sleep(0.5)
        redLED.value(1)
        sleep(1)
        print('.', end="")
    except KeyboardInterrupt: # Ctrl-C
        break

print("\n"+'prog stop')
# remet la LED à 0 (éteinte)
redLED.value(0)