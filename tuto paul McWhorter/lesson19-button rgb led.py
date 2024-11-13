''' Lesson 19 : 3 buttons controls 3 channels R, G and B on a RGB led
                non testé et code partiel ! (surement non fonctionnel)
'''

from machine import Pin
from time import sleep
ledR=Pin(9, Pin.OUT)
ledG=Pin(11, Pin.OUT)
ledB=Pin(10, Pin.OUT)
# je n'ai pas changé le montage donc je met tous les 3 sur le même PIN, c'est juste pour avoir le code
myRedButton=Pin(17, Pin.IN, Pin.PULL_UP)
myGreenButton=Pin(17, Pin.IN, Pin.PULL_UP) # Pin.PULL_UP indique que l'on veut que cette pin soit relié à un courant de 3.3V et une résistance de 10 ohm
myBlueButton=Pin(17, Pin.IN, Pin.PULL_UP)
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
ledR.off() ; ledG.off() ; ledB.off()