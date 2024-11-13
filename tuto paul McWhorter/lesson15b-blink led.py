''' Lesson 15 : blink led
'''

from machine import Pin
from time import sleep
led=Pin(15, Pin.OUT)
while True:
    blinks=1
    numBlinks=int(input('how many blinks? '))
    if numBlinks=='q': break;
    while blinks<=numBlinks:
        led.on()
        sleep(0.5)
        led.off()
        sleep(0.5)
        blinks+=1
print('prog end')