''' Lesson 12 led RGB
'''
from machine import Pin,PWM
from time import sleep
from pgtools import *
# attention chaque patte R, G et B de la LED doit avoir sa propre résistance !
ledR=PWM(Pin(9))
ledG=PWM(Pin(11))
ledB=PWM(Pin(10))
ledR.freq(1000) ; ledR.duty_u16(0)
ledG.freq(1000) ; ledG.duty_u16(0)
ledB.freq(1000) ; ledB.duty_u16(0)

linCv = LinearConverter(272, 65535, 0, 65535)
while (True):
    try:
        rBright=0
        gBright=15000
        bBright=0
        ledR.duty_u16(rBright)
        ledG.duty_u16(gBright)
        ledB.duty_u16(bBright)
        sleep(.1)
    except KeyboardInterrupt: # Ctrl-C
        break

print("\n"+'prog end')
ledR.duty_u16(0) ; ledG.duty_u16(0) ; ledB.duty_u16(0)