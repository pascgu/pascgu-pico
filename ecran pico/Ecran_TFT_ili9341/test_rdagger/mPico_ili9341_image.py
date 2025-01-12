"""
Raspperry Pi Pico exercise display on ili9341 SPI Display
using rdagger/micropython-ili9341,
MicroPython ILI9341 Display and XPT2046 Touch Screen Drivers
https://github.com/rdagger/micropython-ili9341
"""
from machine import Pin, SPI
import utime

import ili9341
from xglcd_font import XglcdFont

import mySetup

print(SPI(0))
print(SPI(1))

display = mySetup.createMyDisplay()

#print('Loading fonts...')
#print('Loading unispace')
#unispace = XglcdFont('fonts/Unispace12x24.c', 12, 24)
#unispace = XglcdFont('Unispace12x24.c', 12, 24)

#display.draw_image('fruit2_300x200.raw', 0, 0, 300, 200)
#display.draw_image('fruit2_320x480.raw', 0, 0, 320, 480)
display.draw_image('fruit2_480x320.raw', 0, 0, 480, 320) # fonctionne après avoir corrigé la lib ili9341.py !!! Donc bien utiliser cette-ci corrigée
#display.draw_image('fruits.raw', 0, 0, 320, 400)

# PG important : Pour générer les images, il faut lancer le script rdagger_micropython-ili9341/utils/img2rgb565.py
#               Se mettre dans une commande "activate pico" :
# (pico) C:\Users\hotma\source\repos\pascgu-pico\tests ext\ecranTFT\rdagger_micropython-ili9341\utils>python img2rgb565.py fruit2_320x480.png 
# Saved: fruit2_320x480.raw


for i in range(320):
    display.scroll(i)
    utime.sleep(0.02)
    
for i in range(320, 0, -1):
    display.scroll(i)
    utime.sleep(0.02)

utime.sleep(2)
# Display inversion on -> NON off (car par défaut je l'inverse lors du mySetup)
display.invert(False)
utime.sleep(2)
# Display inversion off -> NON on
display.invert(True)
utime.sleep(1)

#while True:
#    pass

display.cleanup()
print("- bye -")