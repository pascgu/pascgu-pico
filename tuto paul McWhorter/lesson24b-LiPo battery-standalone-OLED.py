''' Lesson 24b : Power portable projects with LiPo Rechargeable Battery
    Pour le rendre autonome, il faut déjà uploader ce fichier sur le pico avec le nom main.py,
    c'est plus simple d'utiliser Thonny pour ça, qui permet aussi de supprimer le main.py sur le pico après.
    Dans Thonny, ouvrir ce fichier puis Fichier->Enregistrer Sous...->RP2040 device->main.py

    On remplace le LCD par l'OLED
'''

from machine import Pin,I2C
from ssd1306 import SSD1306_I2C
from ssd1306wFont import SSD1306_TOOLS
import utime as time
from dht import DHT11

myPin=Pin(16, Pin.OUT, Pin.PULL_DOWN) # Pin.PULL_DOWN indique que l'on veut que cette pin soit relié à GND et une résistance entre 50k-80k Ohm
sensor=DHT11(myPin)
myButton=Pin(17, Pin.IN, Pin.PULL_UP) # Pin.PULL_UP indique que l'on veut que cette pin soit relié à un courant de 3.3V et une résistance de 10 ohm
i2c0=0
i2c=I2C(i2c0, sda=Pin(20), scl=Pin(21), freq=400000)
dsp=SSD1306_I2C(128,64,i2c) # VCC=3.3V on Pin(3V3 OUT)
dsp_tools=SSD1306_TOOLS(dsp)

tempUnitC=True  # True=°C False=°F
buttonState=1
buttonStateOld=1

print("My sensor values (l24b):")
while True:
    try:
        buttonState=myButton.value()
        if buttonStateOld==0 and buttonState==1: # only on the first Pull up
            tempUnitC = not tempUnitC # switch between °C and °F

        try:
            sensor.measure() # je pense qu'on déclenche la mesure du capteur avant de récupérer les valeurs mesurées
        except:
            continue # J'ajoute ceci car ça ne fonctionne pas quand on en fait un main.py
        tempC=sensor.temperature()
        tempF=tempC*9/5+32 # convert to °F
        hum=sensor.humidity()
        if tempUnitC==True:
            print(f"\r temp={tempC}°C humidity={hum}%", end='') # end='   ' avec des espaces car l'autre affichage va + loin et on veut effacer ces derniers chars
            dsp_tools.prnt_st(f"Temperature = {tempC}\xF8C",0, 0, 1, 1) # "\xF8" signifie "°" dans la font étendue
        else:
            print(f"\r temp={tempF}{chr(176)}F humidity={hum}%", end='') # "\r" et end='' : pour ré-afficher sur la même ligne.
            dsp_tools.prnt_st(f"Temperature = {tempF}\xF8F",0, 0, 1, 1) # "\xF8" signifie "°" dans la font étendue
        dsp.text(f"Humidity = {hum}%", 0, 8, 1)
        dsp.show()

        time.sleep(.1)
        dsp.fill(0)
        buttonStateOld=buttonState

    except KeyboardInterrupt: # Ctrl-C
        break
print('') # pour qu'un retour à la ligne soit fait
dsp.poweroff()
print('prog end')
