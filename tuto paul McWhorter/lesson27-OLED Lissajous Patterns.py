''' Lesson 27 : Creating Lissajous Patterns on an OLED Display
'''

from machine import Pin,I2C
from ssd1306 import SSD1306_I2C
import time
import math
i2c0=0
i2c=I2C(i2c0, sda=Pin(20), scl=Pin(21), freq=400000)
dsp=SSD1306_I2C(128,64,i2c)

try:
    r=35
    xCenter=128/2
    yCenter=41
    phase=0
    phase_speed=7 # 1 is default speed
    list_nodes=[(2,1),(1,2),(4,3),(5,1),(5,3),(10,3)]
    #nodesH,nodesV=2,1 # chip Horizontal
    #nodesH,nodesV=1,2 # chip Vertical
    #nodesH,nodesV=4,3
    #nodesH,nodesV=5,1
    #nodesH,nodesV=5,3
    i_nodes=0
    i_nodes=5
    while True:
        nodesH,nodesV=list_nodes[i_nodes]
        for deg in range(0,360,1):
            rads=deg*2*3.14/360
            x=int(r*math.cos(nodesV*rads+phase)+xCenter)
            y=int(.65*r*math.sin(nodesH*rads)+yCenter)
            dsp.pixel(x,y,1)
        dsp.show()
        dsp.fill(0) # clear screen
        #phase=phase+1*2*3.14/360
        phase+=phase_speed*2*3.14/360
        if phase>6:
            i_nodes=(i_nodes+1)%len(list_nodes)
            phase=0
except KeyboardInterrupt: # Ctrl-C
    pass

dsp.poweroff()
print('prog end')
