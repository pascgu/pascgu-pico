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
    for _ in range(100000):
        try:
            if lock==None: print('PG1'); break
            with lock:
                #print('1',lock.locked())
                if not led_is_on:
                    myLED.on()
                    print('On', end='')
                    led_is_on=True
                    sleep(.2)
                else: print('already on')
            sleep(1)
        except KeyboardInterrupt:
            # TODO PG : ça ne fonctionne pas, on ne rentre pas dans cette exception
            print('thread1 ends')
            lock=None
            break
def put_led_off():
    global led_is_on, lock
    for _ in range(100000):
        if lock==None:
            print('thread2 ends')
            break
        try:
            with lock:
                #print('2',lock.locked())
                if led_is_on:
                    myLED.off()
                    print('Off', end='')
                    led_is_on=False
                else: print('.', end='')
            sleep(.1)
        except KeyboardInterrupt:
            print('PG2')
            lock=None

print('start thread 2')
_thread.start_new_thread(put_led_off, ()) # thread 2 on core 2

print('continue thread 1')
put_led_on() # thread 1 on core 1

print('prog end')
