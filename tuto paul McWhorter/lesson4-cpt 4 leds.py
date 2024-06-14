''' Lesson 4
'''
from machine import Pin
from time import sleep
led1 = Pin(15, Pin.OUT)
led2 = Pin(14, Pin.OUT)
led3 = Pin(13, Pin.OUT)
led4 = Pin(12, Pin.OUT)
val = 0
while (True):
    try:
        # converti val de décimal en binaire
        val_bit0 = val % 2
        val_bit1 = (val // 2) % 2
        val_bit2 = (val // 4) % 2
        val_bit3 = (val // 8) % 2
        #print("val ", val, " = ", val_bit0, " ", val_bit1, " ", val_bit2, " ", val_bit3)
        print(f"val {val} = {val_bit0} {val_bit1} {val_bit2} {val_bit3}")
        led1.value(val_bit0)
        led2.value(val_bit1)
        led3.value(val_bit2)
        led4.value(val_bit3)
        sleep(0.3)
        val += 1
        if val >= 16: val=0
    except KeyboardInterrupt: # Ctrl-C
        break

print("\n"+'prog stop')
# remet la LED à 0 (éteinte)
led1.off()
led2.off()
led3.off()
led4.off()