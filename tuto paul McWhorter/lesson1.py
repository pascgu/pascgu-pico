''' Lesson 1 : tuto https://www.youtube.com/watch?v=C_xiDka0Nm0&list=PLGs0VKk2DiYz8js1SJog21cDhkBqyAhC5&index=1
'''

'''
print('Hello world')

a=7
b=2
c=a*b
print(c)
'''

from machine import Pin
from time import sleep
myLED=Pin('LED',Pin.OUT)
#myLED.value(1) # == myLED.on()
#myLED.value(0) # == myLED.off()

#while (True):
#    myLED.value(1) # == myLED.on()
#    sleep(.1)
#    myLED.value(0) # == myLED.off()
#    sleep(.5)
    
while (True):
    myLED.toggle()
    sleep(.1)
    # sleep(.02) # min value for max blinking LED I can see