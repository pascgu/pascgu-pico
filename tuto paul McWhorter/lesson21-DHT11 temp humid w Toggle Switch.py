''' Lesson 21 : Temperature and Humidity Measurements with Toggle Switch
'''

from machine import Pin
import utime as time
from dht import DHT11

# Dans la vidéo, Ici on va mettre la Pin en OUT alors qu'on va lire dessus, pourquoi ? Parce qu'on veut utiliser un pull down resistor.
#   c'est contre-intuitif mais c'est volontaire et géré correctement ensuite par la lib DHT11.
# myPin=Pin(16, Pin.OUT, Pin.PULL_DOWN) # Pin.PULL_DOWN indique que l'on veut que cette pin soit relié à GND et une résistance entre 50k-80k Ohm
# En fait ça fait une erreur et pour corriger il faut remettre Pin.IN, va savoir...
myPin=Pin(16, Pin.IN, Pin.PULL_DOWN) # Pin.PULL_DOWN indique que l'on veut que cette pin soit relié à GND et une résistance entre 50k-80k Ohm
sensor=DHT11(myPin)
myButton=Pin(17, Pin.IN, Pin.PULL_UP) # Pin.PULL_UP indique que l'on veut que cette pin soit relié à un courant de 3.3V et une résistance de 10 ohm

tempUnitC=True  # True=°C False=°F
buttonState=1
buttonStateOld=1

print("My sensor values (l21):")
while True:
    try:
        buttonState=myButton.value()
        if buttonStateOld==0 and buttonState==1: # only on the first Pull up
            tempUnitC = not tempUnitC # switch between °C and °F

        sensor.measure() # je pense qu'on déclenche la mesure du capteur avant de récupérer les valeurs mesurées
        tempC=sensor.temperature()
        tempF=tempC*9/5+32 # convert to °F
        hum=sensor.humidity()
        if tempUnitC==True:
            print(f"\r temp={tempC}{chr(176)}C humidity={hum}%", end='   ') # end='   ' avec des espaces car l'autre affichage va + loin et on veut effacer ces derniers chars
        else:
            print(f"\r temp={tempF}{chr(176)}F humidity={hum}%", end='') # "\r" et end='' : pour ré-afficher sur la même ligne.
        time.sleep(.3)
        buttonStateOld=buttonState
    except KeyboardInterrupt: # Ctrl-C
        break
print('') # pour qu'un retour à la ligne soit fait
print('prog end')
