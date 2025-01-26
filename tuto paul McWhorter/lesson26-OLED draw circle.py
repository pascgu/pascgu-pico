''' Lesson 26 : Drawing a Circle on the OLED 1306 Display
'''

from machine import Pin,I2C
from ssd1306 import SSD1306_I2C
from time import sleep
import math
i2c0=0
i2c=I2C(i2c0, sda=Pin(20), scl=Pin(21), freq=400000)
dsp=SSD1306_I2C(128,64,i2c)

try:
    r=20
    xCenter=128/2
    yCenter=64/2+8 # on décalle un peu le cercle sinon il passe dans le jaune
    for deg in range(0,360,2): # ici j'ai mis un step 2 au lieu de 1 pour accélérer un peu sans trop changer le résultat.
        rads=deg*2*3.14/360 # convert degree to radian
        x=r*math.cos(rads)+xCenter
        y=-r*math.sin(rads)+yCenter
        dsp.pixel(int(x),int(y),1)
        dsp.show() # évidemment si on ne met pas celui-ci mais celui principal on ne verra pas le cercle se dessiner, c'est instantanné.
    dsp.show()

    dsp.fill(0) # clear all screen

    rStart=5
    rStop=25
    xCenter=128/2
    yCenter=64/2+8 # on décalle un peu le cercle sinon il passe dans le jaune
    for r in range(rStart,rStop,1):
        for deg in range(0,360,1):
            rads=deg*2*3.14/360 # convert degree to radian
            x=r*math.cos(rads)+xCenter
            y=-r*math.sin(rads)+yCenter
            dsp.pixel(int(x),int(y),1)
            #dsp.show() # évidemment si on ne met pas celui-ci mais celui principal on ne verra pas le cercle se dessiner, c'est instantanné.
        dsp.show()
    dsp.show()
    
    sleep(1)
    dsp.fill(0) # clear all screen

    # avec celui-ci on pourrai imaginer faire une jauge
    rStart=18
    rStop=25
    xCenter=128/2
    yCenter=64/2+8 # on décalle un peu le cercle sinon il passe dans le jaune
    for r in range(rStart,rStop,1):
        for deg in range(-40,220,1):
            rads=deg*2*3.14/360 # convert degree to radian
            x=r*math.cos(rads)+xCenter
            y=-r*math.sin(rads)+yCenter
            dsp.pixel(int(x),int(y),1)
            #dsp.show() # évidemment si on ne met pas celui-ci mais celui principal on ne verra pas le cercle se dessiner, c'est instantanné.
        dsp.show()
    dsp.show()
except KeyboardInterrupt: # Ctrl-C
    pass

sleep(2)
dsp.poweroff()
print('prog end')
