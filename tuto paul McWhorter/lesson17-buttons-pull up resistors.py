''' Lesson 17 : buttons and pull up resistors
'''

from machine import Pin
from time import sleep
myButton=Pin(17, Pin.IN, Pin.PULL_UP) # Pin.PULL_UP indique que l'on veut que cette pin soit relié à un courant de 3.3V et une résistance de 10 ohm
while True:
    try:
        butState=myButton.value() # return 1 if button not pressed and 0 if pressed
        print(butState)
        sleep(.1)
    except KeyboardInterrupt: # Ctrl-C
        break

print('prog end')