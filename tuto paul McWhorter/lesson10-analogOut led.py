''' Lesson 10 analog output
'''
from machine import Pin, PWM
from time import sleep
from pgtools import *
outPin=16
analogOut=PWM(Pin(outPin))
analogOut.freq(1000) # 1kHz
analogOut.duty_u16(0)

linCv = LinearConverter(0, 3.3, 0, 65535)

while (True):
    try:
        ret=input('What Voltage (0V-3.3V) ? ')
        if ret=='q': break
        myVoltage=float(ret)
        pwmVal=linCv.conv(myVoltage)
        #print(pwmVal)
        analogOut.duty_u16(int(pwmVal))
    except KeyboardInterrupt: # Ctrl-C
        break

analogOut.duty_u16(0)
print("\n"+'prog end')
