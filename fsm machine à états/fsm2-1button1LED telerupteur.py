''' fsm2 : exemple de machine à état avec 1 bouton et 1 led (cf drawio fsm2). 4 états : Off1/On1/On2/Off2. Transitions: Off1->bt1 up->On1->bt1 down->On2->bt1 up->Off2->bt1 down->Off1
    C'est une machine à état de système synchrone car le test des transitions est fait de manière synchrone toutes les X millisecondes.
    exemple créé à partir de lesson18 et des vidéos suivantes :
    https://www.youtube.com/watch?v=HJx3DeW7J4Q (FR)
    https://www.youtube.com/watch?v=Ar1CYfRxs38&list=PLEVjCycRK1D0YvSf9bTjISthjLdoXacy8&index=20 (FR codé en C)
    https://www.youtube.com/watch?v=p1gv4x01zNQ (FR codé en unity)
    https://www.youtube.com/watch?v=E45v2dD3IQU (EN codé en python)
'''

from machine import Pin
from time import sleep
button1 = Pin(17, Pin.IN, Pin.PULL_UP) # Pin.PULL_UP indique que l'on veut que cette pin soit relié à un courant de 3.3V et une résistance de 10 ohm. L'autre patte du bouton relié à GND.
led = Pin(12, Pin.OUT)
wait_seconds = 0.1 # délai entre 2 boucles de refresh des états et test des transitions

class SState():
    _val:int=0
    def val(self) -> int:
        return self._val
    def __str__(self) -> str:
        return f"{self.__class__.__name__}#{self._val}"
class StateOff1(SState): _val=1
class StateOn1(SState):  _val=2
class StateOn2(SState):  _val=3
class StateOff2(SState): _val=4

class State():
    Off1 = StateOff1()
    On1  = StateOn1()
    On2  = StateOn2()
    Off2 = StateOff2()

def run_state(state:SState):
    '''fonction qui exécute l'état'''
    global led
    if state == State.Off1 or state == State.Off2:
        led.value(False)
    elif state == State.On1 or state == State.On2:
        led.value(True)

def change_state(state:SState):
    '''fonction qui réalise le changement d'état.
        Cette fonction n'a pas beaucoup d'intérêt sauf pour réaliser des opérations quand on entre ou qu'on quitte un état
    '''
    global current_state
    if current_state != state:
        leave_state(current_state) # avant de changer, on quitte l'ancien état

        # change l'état
        print(f"change d'etat de {current_state} -> {state}")
        current_state = state
        
        enter_state(state) # après avoir changé, on entre dans le nouvel état

def enter_state(state:SState):
    '''point d'entrée où on peut exécuter des choses quand on entre dans l'état'''
    
def leave_state(state:SState):
    '''point d'entrée où on peut exécuter des choses quand on sort de l'état'''
    

def transitions():
    '''fonction qui teste s'il y a des transitions déclenchées et si c'est le cas change d'état'''
    global current_state, button1
    bt1_pressed = not button1.value() # car PULL_UP, défaut 1 et si enfoncé 0
    new_state = None
    if current_state == State.Off1:
        if bt1_pressed: new_state = State.On1
    elif current_state == State.On1:
        if not bt1_pressed: new_state = State.On2
    elif current_state == State.On2:
        if bt1_pressed: new_state = State.Off2
    elif current_state == State.Off2:
        if not bt1_pressed: new_state = State.Off1
    
    if new_state != None:
        change_state(new_state)


############### MAIN #################

current_state:SState = State.Off1 # init
print('prog start')
while True:
    try:
        run_state(current_state) # refresh l'état en cours
        transitions()            # vérifie s'il y a des transitions
        sleep(wait_seconds)
    except KeyboardInterrupt: # Ctrl-C
        break

print('prog end')
led.off()