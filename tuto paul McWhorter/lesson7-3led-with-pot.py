''' Lesson 7
'''
from machine import Pin, ADC
from time import sleep
from pgtools import *
potPin=28 # ADC2 == GP28
myPot = ADC(potPin) # analog IN, 3 pins possibles : ADC0, ADC1, ADC2
led1 = Pin(15, Pin.OUT) #green
led2 = Pin(14, Pin.OUT) #yellow
led3 = Pin(13, Pin.OUT) #red

x1=250 ; x2=65535 # pot min and max values found when testing
y1=0   ; y2=100   # target min and max values to convert to
linCv = LinearConverter(x1,x2,y1,y2)
while (True):
    try:
        potVal = myPot.read_u16() # read analog value between 0 and 65535
        voltage = linCv.conv(potVal)
        print(potVal, voltage)

        if (voltage < 80):      led1.on(); led2.off();led3.off()
        elif (voltage < 95):    led1.off();led2.on(); led3.off()
        else :                  led1.off();led2.off();led3.on()
        sleep(0.1)
    except KeyboardInterrupt: # Ctrl-C
        break

print("\n"+'prog stop')
led1.off()
led2.off()
led3.off()