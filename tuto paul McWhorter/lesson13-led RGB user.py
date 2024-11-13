''' Lesson 13 led RGB
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
        strColor=input('Choisir une couleur: rouge,vert,bleu,cyan,magenta,yellow,orange,blanc,noir (q=quit): ')
        if strColor=='q': break
        if strColor=='rouge':
            rBright=65535 ; gBright=0 ; bBright=0
        elif strColor=='vert':
            rBright=0 ; gBright=65535 ; bBright=0
        elif strColor=='bleu':
            rBright=0 ; gBright=0 ; bBright=65535
        elif strColor=='cyan':
            rBright=0 ; gBright=65535 ; bBright=65535
        elif strColor=='magenta':
            rBright=65535 ; gBright=0 ; bBright=65535
        elif strColor=='jaune':
            rBright=65535 ; gBright=65535 ; bBright=0
        elif strColor=='orange':
            rBright=65535 ; gBright=10000 ; bBright=0
        elif strColor=='blanc':
            rBright=65535 ; gBright=65535 ; bBright=65535
        elif strColor=='noir':
            rBright=0 ; gBright=0 ; bBright=0

        ledR.duty_u16(rBright)
        ledG.duty_u16(gBright)
        ledB.duty_u16(bBright)
    except KeyboardInterrupt: # Ctrl-C
        break

print("\n"+'prog end')
ledR.duty_u16(0) ; ledG.duty_u16(0) ; ledB.duty_u16(0)