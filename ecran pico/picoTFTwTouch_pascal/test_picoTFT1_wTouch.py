from machine import Pin, SPI
from sys import implementation
from os import uname
from utime import sleep, ticks_us, ticks_diff
from ili9341 import color565
# import ili9341, gt911, gt911_constants as gt # PG: je le laisse ici pour ne pas oublier d'upload ces 3 fichiers .py
from collections import deque
from picoTFTwTouch import *

green = color565(0,255,0)

points:deque[tuple[int,int]]=deque((),100)
last_t_us = ticks_us()
def on_touch_interrupt(buff_points, n): # s'exécute environ tous les 10_000 us
    # ici on est dans un callback d'interruption. Donc le minimum: remplir une queue mais pas d'objets, juste d'un tuple (même un namedtuple ça pompe trop)
    global TFT, points, green, last_t_us
    if n:
        #t_us = ticks_us() ; print(f"Received touch events: ({ticks_diff(t_us,last_t_us)})") ; last_t_us = t_us
        for i in range(n):
            point = buff_points[i]
            points.append((point.x,point.y))
    else: # il peut parfois être utile de gérer quand on relève le doigt et dans ce cas, il y a 3 on_touch sans point.
        t_us = ticks_us() ; print(f"NO POINTS !!! ({ticks_diff(t_us,last_t_us)})") ; last_t_us = t_us

TFT = picoTFTwTouch(on_touch_interrupt)

try:
    while True:
        if points:
            x,y = points.popleft()
            #print(f"  Touch: {x},{y}")
            TFT.display.fill_circle(x, y, 2, green)
except KeyboardInterrupt:
    pass

TFT.cleanup()
print("- bye -")