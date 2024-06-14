import bootsel
import time

def WaitForPushed():
    while bootsel.button() == 0:
        time.sleep(0.1)
    print("BOOTSEL Pushed")

def WaitForRelease():
    while bootsel.button() == 1:
        time.sleep(0.1)
    print("BOOTSEL Released")

if bootsel.button() == 1:
    print("BOOTSEL Pushed")
    WaitForRelease()
else:
    print("BOOTSEL Not Pushed")
    
while True:
    WaitForPushed()
    WaitForRelease()
