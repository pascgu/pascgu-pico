"""
Raspperry Pi Pico exercise display on ili9341 SPI Display
using rdagger/micropython-ili9341,
MicroPython ILI9341 Display and XPT2046 Touch Screen Drivers
https://github.com/rdagger/micropython-ili9341
"""
from machine import Pin, SPI
import utime

import ili9341
#from xglcd_font import XglcdFont

import mySetup

print(SPI(0))
print(SPI(1))

display = mySetup.createMyDisplay()

#display.cleanup()

#print('Loading fonts...')
#print('Loading unispace')
#unispace = XglcdFont('fonts/Unispace12x24.c', 12, 24)
#unispace = XglcdFont('Unispace12x24.c', 12, 24)

#display.draw_image('fruit2_300x200.raw', 0, 0, 300, 200)
#display.draw_image('fruit2_320x480.raw', 0, 0, 320, 480)
#display.draw_image('fruits.raw', 0, 0, 320, 400)
display.draw_image('fruit2_480x320.raw', 0, 0, 480, 320) # fonctionne après avoir corrigé la lib ili9341.py !!! Donc bien utiliser cette-ci corrigée
#display.draw_image('fruit2_480x320v2.bin', 0, 0, 480, 320)
#display.draw_image('fruit2_300x200CF_RGB565A8.bin', 0, 0, 300, 200)
#display.draw_image('fruit2_300x200CF_RGB565A8swap.bin', 0, 0, 300, 200)
# display.draw_image('fruit2_100x67CF_ALPHA_1_BIT.bin', 0, 0, 67, 100)
# display.draw_image('fruit2_100x67CF_ALPHA_2_BIT.bin', 0, 0, 67, 100)
# display.draw_image('fruit2_100x67CF_ALPHA_4_BIT.bin', 0, 0, 67, 100)
# display.draw_image('fruit2_100x67CF_ALPHA_8_BIT.bin', 0, 0, 67, 100)
# display.draw_image('fruit2_100x67CF_INDEXED_1_BIT.bin', 0, 0, 67, 100)
# display.draw_image('fruit2_100x67CF_INDEXED_2_BIT.bin', 0, 0, 67, 100)
# display.draw_image('fruit2_100x67CF_INDEXED_4_BIT.bin', 0, 0, 67, 100)
# display.draw_image('fruit2_100x67CF_INDEXED_8_BIT.bin', 0, 0, 67, 100)
# display.draw_image('fruit2_100x67CF_RAW_ALPHA.bin', 0, 0, 100, 67)
# display.draw_image('fruit2_100x67CF_RAW_CHROMA.bin', 0, 0, 100, 67)
# display.draw_image('fruit2_100x67CF_RAW.bin', 0, 0, 67, 100)
# display.draw_image('fruit2_100x67CF_RGB565A8.bin', 0, 0, 100, 67)
# display.draw_image('fruit2_100x67CF_TRUE_COLOR_ALPHA.bin', 0, 0, 100, 67)
# display.draw_image('fruit2_100x67CF_TRUE_COLOR_CHROMA.bin', 0, 0, 100, 67)
# display.draw_image('fruit2_100x67CF_TRUE_COLOR.bin', 0, 0, 100, 67)
#display.draw_image('fruit2_100x67CF_RGB565A8big.bin', 0, 0, 100, 67)

#display.draw_image('fruit2_100x67.raw', 0, 0, 100, 67) # fonctionne
#display.draw_image('fruit2_100x67_transpPNG.raw', 0, 0, 100, 67) # fonctionne
# display.draw_image('fruit2_100x67_transpJPG.raw', 0, 0, 100, 67) # pas la transparence
#display.draw_image('fruit2_100x67_transp.raw', 0, 0, 100, 67) # fonctionne
#display.draw_image('rgb.raw', 0, 0, 100, 67) # fonctionne

# NON!!! PG important : Pour générer les images, il faut lancer le script img2rgb565inv.py (nouvelle version de img1rgb565.py qui inverse les bits)

# PG important : Pour générer les images, il faut lancer le script img1rgb565.py
#               Se mettre dans une commande "activate pico" :
# (pico) C:\Users\hotma\source\repos\pascgu-pico\ecran pico\Ecran_TFT_ili9341\test_rdagger>python img2rgb565.py ..\fruit2_480x320.png
# Saved: ..\fruit2_480x320.raw

for i in range(320):
    display.scroll(i)
    utime.sleep(0.02)
    
for i in range(320, 0, -1):
    display.scroll(i)
    utime.sleep(0.02)

utime.sleep(2)
# Display inversion off. PG: car déjà on lors de l'init
display.invert(False)
utime.sleep(2)
# Display inversion on
display.invert(True)
utime.sleep(1)

#while True:
#    pass

display.cleanup()
print("- bye -")