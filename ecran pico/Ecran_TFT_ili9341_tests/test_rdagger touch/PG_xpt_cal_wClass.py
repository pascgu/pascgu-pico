from machine import Pin, SPI
from sys import implementation
from os import uname
from utime import sleep
# import ili9341, gt911, gt911_constants as gt # PG: je le laisse ici pour ne pas oublier d'upload ces 3 fichiers .py
from colors import *
from picoTFTwTouch import *

print(implementation.name) # type: ignore
print(uname()[3])
print(uname()[4])

print(SPI(0))
print(SPI(1))

def on_touch(points):
    global picoTFT
    
    if points:
        print("Received touch events:")
        for i, point in enumerate(points):
            print(f"  Touch {i+1}: {point.x}, {point.y}, size: {point.size}")
            picoTFT.display.fill_circle(point.x, point.y, 2, green)

def redraw_ui():
    print("Redraw UI")
    picoTFT.redraw()

bt2_i=0
def bt2_clicked(bt):
    global bt2_i
    print(f"Button2 clicked {bt2_i} times")
    bt2_i+=1

picoTFT = picoTFTwTouch(on_touch)
bt1 = Button(Rect(0,0,100,48), "button1", lambda bt: redraw_ui())
bt2 = Button(Rect(0,50,100,48), "auto-click", bt2_clicked)
picoTFT.addButtons([bt1,bt2])
redraw_ui()

try:
    while True:
        sleep(0.01)
except KeyboardInterrupt:
    pass

picoTFT.cleanup()
print("- bye -")