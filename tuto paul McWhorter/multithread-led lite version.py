''' Tests multithread led : https://www.youtube.com/watch?v=QeDnjcdGrpY&list=TLPQMTMwNjIwMjTDImmxcK5bYA
'''

from machine import Pin
from time import sleep
import _thread
myLED=Pin('LED',Pin.OUT)
led_is_on=False
lock=_thread.allocate_lock() # mutex

def put_led_on():
    global led_is_on, lock
    while True:
        with lock:
            if not led_is_on:
                myLED.on()
                print('On', end='')
                led_is_on=True
                sleep(.2)
            else: print('already on')
        sleep(1)

def put_led_off():
    global led_is_on, lock
    while True:
        with lock:
            if led_is_on:
                myLED.off()
                print('Off', end='')
                led_is_on=False
            else: print('.', end='')
        sleep(.1)

print('start thread 2')
_thread.start_new_thread(put_led_off, ()) # thread 2 on core 2
# sur un pico, on ne peut pas faire + de 2 threads en même temps, un sur chaque core.

print('continue thread 1')
put_led_on() # thread 1 on core 1

print('prog end')
