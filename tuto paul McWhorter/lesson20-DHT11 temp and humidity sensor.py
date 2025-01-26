''' Lesson 20 : DHT 11 temperature and humidity sensor
'''

from machine import Pin
import utime as time
from dht import DHT11

# Dans la vidéo, Ici on va mettre la Pin en OUT alors qu'on va lire dessus, pourquoi ? Parce qu'on veut utiliser un pull down resistor.
#   c'est contre-intuitif mais c'est volontaire et géré correctement ensuite par la lib DHT11.
myPin=Pin(16, Pin.OUT, Pin.PULL_DOWN) # Pin.PULL_DOWN indique que l'on veut que cette pin soit relié à GND et une résistance entre 50k-80k Ohm
# En fait ça fait une erreur et pour corriger il faut remettre Pin.IN, va savoir pourquoi?
# myPin=Pin(16, Pin.IN, Pin.PULL_DOWN) # Pin.PULL_DOWN indique que l'on veut que cette pin soit relié à GND et une résistance entre 50k-80k Ohm
#   => En fait NONNNN ! il faut juste faire un 1er sensor.measure() sans exception et laisser le Pin.OUT sinon ça bug quand on transforme en main.py
sensor=DHT11(myPin)

try: sensor.measure() # pour éviter erreur de sensor.measure() : OSError: [Errno 110] ETIMEDOUT
except: pass

print("My sensor values:")
while True:
    try:
        sensor.measure() # je pense qu'on déclenche la mesure du capteur avant de récupérer les valeurs mesurées
        tempC=sensor.temperature()
        hum=sensor.humidity()
        #print(f"temp={tempC}°C humidity={hum}%")
        print(f"\r temp={tempC}°C humidity={hum}%", end='') # "\r" et end='' : pour ré-afficher sur la même ligne
        time.sleep(1)
    except KeyboardInterrupt: # Ctrl-C
        break
print('') # pour qu'un retour à la ligne soit fait
print('prog end')
