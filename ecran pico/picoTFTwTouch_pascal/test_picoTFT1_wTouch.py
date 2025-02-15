from machine import Pin, SPI
from sys import implementation
from os import uname
from utime import sleep
from ili9341 import color565
# import ili9341, gt911, gt911_constants as gt # PG: je le laisse ici pour ne pas oublier d'upload ces 3 fichiers .py
from picoTFTwTouch import *

def on_touch(points):
    # ici on est dans un callback d'interruption
    global TFT
    if points:
        print("Received touch events:")
        for i, point in enumerate(points):
            print(f"  Touch {i+1}: {point}")
            TFT.display.fill_circle(point.x, point.y, 2, color565(0,255,0))
    #else: # il peut parfois être utile de gérer quand on relève le doigt et dans ce cas, il y a un on_touch sans point.

TFT = picoTFTwTouch(on_touch)

try:
    while True:
        pass
except KeyboardInterrupt:
    pass

TFT.cleanup()
print("- bye -")