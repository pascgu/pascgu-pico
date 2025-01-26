''' Lesson 23 : Temperature and Humidity Sensor with LCD
'''

from machine import Pin
import utime as time
from dht import DHT11
from lcd1602 import LCD

myPin=Pin(16, Pin.OUT, Pin.PULL_DOWN) # Pin.PULL_DOWN indique que l'on veut que cette pin soit relié à GND et une résistance entre 50k-80k Ohm
sensor=DHT11(myPin)
myButton=Pin(17, Pin.IN, Pin.PULL_UP) # Pin.PULL_UP indique que l'on veut que cette pin soit relié à un courant de 3.3V et une résistance de 10 ohm
lcd=LCD() # SDA=Pin(6), SCL=Pin(7), VCC=5V

tempUnitC=True  # True=°C False=°F
buttonState=1
buttonStateOld=1

try: sensor.measure() # pour éviter erreur de sensor.measure() : OSError: [Errno 110] ETIMEDOUT
except: pass

print("My sensor values (l23):")
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
            print(f"\r temp={tempC}°C humidity={hum}%", end='   ') # end='   ' avec des espaces car l'autre affichage va + loin et on veut effacer ces derniers chars
            lcd.write(0,0,f"Temp = {tempC}\xDFC    ") # "\xDF" signifie "°" sur le LCD
        else:
            print(f"\r temp={tempF}{chr(176)}F humidity={hum}%", end='') # "\r" et end='' : pour ré-afficher sur la même ligne.
            lcd.write(0,0,f"Temp = {tempF}\xDFF    ")
        lcd.write(0,1,f"Humidity = {hum}%      ")

        time.sleep(.3)
        buttonStateOld=buttonState

    except KeyboardInterrupt: # Ctrl-C
        break
print('') # pour qu'un retour à la ligne soit fait
lcd.clear()
print('prog end')
