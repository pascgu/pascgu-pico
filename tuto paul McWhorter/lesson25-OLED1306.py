''' Lesson 25 : Getting Started with OLED 1306 in Micropython
    download ssd1306.py from : https://github.com/stlehmann/micropython-ssd1306
    Si erreur [Errno 5] EIO, File "ssd1306.py", line 115, in write_cmd :
        installer le scanner pour trouver les périph i2c : https://randomnerdtutorials.com/raspberry-pi-pico-i2c-scanner-micropython/
'''

from machine import Pin,I2C
from ssd1306 import SSD1306_I2C
import time
i2c1=1 # channel i2c0 or i2c1. Plein de gens ont des soucis avec l'i2c0 sur picoW donc on utilise le 1.
i2c0=0 # PG: Ben dans mon cas, impossible de faire marcher i2c1 mais le 0 fonctionne !
#i2c=I2C(i2c1, sda=Pin(26), scl=Pin(27), freq=400000)
#i2c=I2C(i2c1, sda=Pin(6), scl=Pin(7), freq=400000)
#i2c=I2C(i2c0, sda=Pin(0), scl=Pin(1), freq=400000)
i2c=I2C(i2c0, sda=Pin(20), scl=Pin(21), freq=400000)

oled_i2c_addr = 0x3c # ATTENTION : pour trouver ceci, lancer le scanner lesson25.pre-scanner I2C.py
# PG: dans mon cas, 0x3c=60, c'est l'adresse par défaut donc pas besoin de la préciser.
#dsp=SSD1306_I2C(128,64,i2c,addr=oled_i2c_addr)

# 128x64 (128 columns x 64 rows).
# Dont les 2 premières lignes sont en jaune (donc les pixels 0 à 15), les autres en bleu (px 16 à 63).
# Il y a un espace entre les pixels 15 et 16, donc pas possible de faire une forme en partie jaune et bleu.
dsp=SSD1306_I2C(128,64,i2c) # VCC=3.3V on Pin(3V3 OUT)

msg='Hello world!'
x_px,y_px=0,0 # coord x,y different than col,row because each char take 8x8 pixels
dsp.text(msg,x_px,y_px)
dsp.text('je teste Ligne3',0,16) # 16=8*2 (donc ligne 3 qui est bleue), on peut biensur afficher le texte au pixel 17 ou 18...
dsp.pixel(64,32,1) # pixel au milieu de l'écran, c>=1 allumé, c=0 éteint, cet écran ne gère pas les couleurs)
dsp.hline(20,25,40,1) # draw a horizontal line
dsp.vline(20,25,30,1) # draw a vertical line
dsp.line(20,25, 118,54, 1) # draw a line between 2 points
dsp.rect(64,32,30,20,1) # draw a rectangle
dsp.fill_rect(70,40,15,10,1) # draw and fill a rectangle
dsp.ellipse(26, 31, 5, 5, 1, False) # draw a circle (x,y) est le centre du cercle, rx=ry=rayon du cercle
dsp.ellipse(29, 43, 8, 5, 1, True, 0b0111) # draw an ellipse with fill and only 3 quarters
dsp.show()
try:
    invert=input('Show screen inverted (y/n) ? ')
    if invert in ['y','Y','i','I','o','O']:
        dsp.invert(1)
        time.sleep(2)
        dsp.invert(0)
        time.sleep(1)
    else:
        time.sleep(3)

    dsp.poweroff() 
    time.sleep(1)
    dsp.poweron() # ici ce qui est top, c'est qu'il se souvient de l'image d'avant. Pas besoin de tout redessiner.
    time.sleep(2)
except KeyboardInterrupt: # Ctrl-C
    pass

dsp.poweroff()
print('prog end')
