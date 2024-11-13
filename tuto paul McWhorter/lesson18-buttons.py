''' Lesson 18 : button start/stop a led
'''

from machine import Pin
from time import sleep
myButton=Pin(17, Pin.IN, Pin.PULL_UP) # Pin.PULL_UP indique que l'on veut que cette pin soit relié à un courant de 3.3V et une résistance de 10 ohm
led=Pin(12, Pin.OUT)
#last_butState=1 # not pressed
last_btPressed=False
ledState=False
while True:
    try:
        butState=myButton.value()
        btPressed=not butState # if butState==1 => le bouton n'est pas enfoncé. Si == 0, il est enfoncé
        #if butState != last_butState and butState>=1: # quand on passe de 0 à 1 (<=> "pressed" à "not pressed")
            #led.toggle()
        if btPressed != last_btPressed and last_btPressed : # quand on passe de "pressed" à "not pressed"
            ledState=not ledState # True=led allumée
            led.value(ledState) # ici ça va simplement convertir l'état que l'on souhaite en 1 ou 0 pour allumer ou éteindre.
        #last_butState=butState
        last_btPressed=btPressed
        sleep(.1)
    except KeyboardInterrupt: # Ctrl-C
        break

print('prog end')
led.off()