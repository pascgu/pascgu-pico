''' Lesson 9 analog output
'''
from machine import Pin, PWM
from time import sleep
from pgtools import *
outPin=16
analogOut=PWM(Pin(outPin))
analogOut.freq(1000) # 1kHz
analogOut.duty_u16(0)

linCv = LinearConverter(0, 3.3, 0, 65535)

while True:
    try:
        myVoltage=float(input('What Voltage would you like ? '))
        pwmVal=linCv.conv(myVoltage)
        analogOut.duty_u16(int(pwmVal))
        #PG : jamais testé. Sur la vidéo il montre la sortie sur un oscillo.
        sleep(.1)
    except KeyboardInterrupt: # Ctrl-C
        break

print("\n"+'prog end')
