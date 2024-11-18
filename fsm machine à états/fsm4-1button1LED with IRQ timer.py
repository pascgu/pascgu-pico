''' fsm4 : 1 seul bouton pour passer dans les 5 états On/Off/Clignotte/OnBegin/OffBegin cf le drawio fsm4.
    Double click sur le bouton pour passer en Clignotte. Le clignotte lance un timer et reboucle sur lui-même pour gérer le clignottement.
    5 états: 3 états stables : Off/On/Clignotte + 2 états intermédiaires : OnBegin/OffBegin.
    Transitions: Off->bt1->OnBegin->timer 1s->On->bt1->OffBegin->timer 1s->Off  et  OnBegin|OffBegin->bt1->Clignotte->bt1->OffBegin.
    Par rapport aux autres, celui-ci ne déclenche pas les run_state régulièrement mais seulement quand on change d'état
      ou au besoin (cas Clignotte run_state dans le timer).
    NOTE PG : je pense que l'idée du "double clic" est à abandonner à cause des rebonds avec l'IRQ. Ca fonctionnerai mieux avec 2 boutons.
    C'est une machine à état de système synchrone car le test des transitions est fait de manière synchrone toutes les X millisecondes.
    exemple créé à partir de lesson18 et des vidéos suivantes :
    https://www.youtube.com/watch?v=HJx3DeW7J4Q (FR)
    https://www.youtube.com/watch?v=Ar1CYfRxs38&list=PLEVjCycRK1D0YvSf9bTjISthjLdoXacy8&index=20 (FR codé en C)
    https://www.youtube.com/watch?v=p1gv4x01zNQ (FR codé en unity)
    https://www.youtube.com/watch?v=E45v2dD3IQU (EN codé en python)
'''

from machine import Pin, Timer
import time
button1 = Pin(17, Pin.IN, Pin.PULL_UP) # Pin.PULL_UP indique que l'on veut que cette pin soit relié à un courant de 3.3V et une résistance de 10 ohm. L'autre patte du bouton relié à GND.
led = Pin(12, Pin.OUT)

wait_seconds = 0.1 # délai entre 2 boucles qui vérifie les transitions et change d'état
clignotte_seconds = 0.4
twice_button_seconds = 1 # délai max entre 2 clics du même bouton
timer_worker:Timer|None = None # contiendra une instance de Timer() dans l'état Clignotte ou les 2 états : OnBegin et OffBegin
button_bounce_seconds = 0.3 # délai au dessous duquel, on considère que c'est un rebond du bouton (un "faux" appui)
button_bounce_milliseconds = int(button_bounce_seconds * 1000) # =300

class SState():
    val:int
    def __str__(self) -> str:
        return f"{self.__class__.__name__}#{self.val}"
class StateOff(SState): val=1
class StateOn(SState):  val=2
class StateClignotte(SState):  val=3
class StateOnBegin(SState):  val=4
class StateOffBegin(SState): val=5

# Cette classe n'est là que pour clarifier l'utilisation des états et se rapprocher d'un enum (qui n'existe pas en micropython)
class State():
    Off         = StateOff()
    On          = StateOn()
    OnBegin     = StateOnBegin()
    OffBegin    = StateOffBegin()
    Clignotte   = StateClignotte()

def run_state(state:SState):
    '''fonction qui exécute l'état'''
    global current_led_value
    if state == State.Off or state == State.OffBegin:
        led.value(False)
    elif state == State.On or state == State.OnBegin:
        led.value(True)
    elif state == State.Clignotte:
        led.toggle()

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
    global timer_worker, clignotte_seconds, twice_button_seconds, timer_begin_finished
    if state == State.Clignotte:
        timer_worker = Timer()
        timer_worker.init(mode=Timer.PERIODIC, period=int(clignotte_seconds*1000), callback=timer_worker_callback)
    if state == State.OnBegin or state == State.OffBegin:
        timer_worker = Timer()
        timer_worker.init(mode=Timer.ONE_SHOT, period=int(twice_button_seconds*1000), callback=timer_worker_callback)
        timer_begin_finished = False
    
def leave_state(state:SState):
    '''point d'entrée où on peut exécuter des choses quand on sort de l'état'''
    global timer_worker, timer_begin_finished
    if state == State.Clignotte or state == StateOnBegin or state == StateOffBegin:
        if timer_worker != None:
            timer_worker.deinit() # arrête le timer !
            timer_worker = None
            timer_begin_finished = False


def transitions() -> SState | None:
    '''fonction qui teste s'il y a des transitions déclenchées et si c'est le cas change d'état'''
    global current_state, bt1_pressed, timer_begin_finished
    new_state = None
    if current_state == State.Off:
        if bt1_pressed:
            bt1_pressed = 0
            new_state = State.OnBegin
    elif current_state == State.OnBegin:
        if timer_begin_finished:
            timer_begin_finished = False
            new_state = State.On
        elif bt1_pressed:
            bt1_pressed = 0
            new_state = State.Clignotte
    elif current_state == State.On:
        if bt1_pressed:
            bt1_pressed = 0
            new_state = State.OffBegin
    elif current_state == State.Clignotte:
        if bt1_pressed:
            bt1_pressed = 0
            new_state = State.OffBegin
    elif current_state == State.OffBegin:
        if timer_begin_finished:
            timer_begin_finished = False
            new_state = State.Off
        elif bt1_pressed:
            bt1_pressed = 0
            new_state = State.Clignotte

    if new_state != None:
        change_state(new_state)
    return new_state

timer_begin_finished = False
def timer_worker_callback(timer):
    '''fonction appelée à chaque tick du timer (seulement dans l'état Clignotte)
    '''
    global current_state, timer_begin_finished
    if current_state == State.OnBegin or current_state == State.OffBegin:
        timer_begin_finished = True
    if current_state == State.Clignotte:
        run_state(current_state)

bt1_pressed = 0
bt1_clicked_last_time = time.ticks_ms()
def button1_clicked_callback(pin):
    '''fonction appelée lors de l'interruption de l'irq : ici lorsque le button1 est appuyé
    '''
    global bt1_pressed, button_bounce_milliseconds, bt1_clicked_last_time
    bt1_clicked_new_time = time.ticks_ms()
    bt1_clicked_diff_time = time.ticks_diff(bt1_clicked_new_time, bt1_clicked_last_time)
    # gestion du rebond du bouton
    if bt1_clicked_diff_time < button_bounce_milliseconds:
        print(f"IRQ bt1 ignored #{bt1_pressed} f={pin.irq().flags()} diff={bt1_clicked_diff_time}")
        return # ne fait rien, on part du principe que c'est un rebond du bouton qui a déclencher à nouveau ce callback par erreur
    
    bt1_clicked_last_time = bt1_clicked_new_time
    # le bouton a été cliqué 1 fois
    bt1_pressed += 1
    print(f"IRQ bt1 #{bt1_pressed} f={pin.irq().flags()} diff={bt1_clicked_diff_time}")
    


############### MAIN #################

current_state:SState = State.Off # init
# IRQ :
button1.irq(trigger=Pin.IRQ_RISING, handler=button1_clicked_callback) # Définit un IRQ avec callback button1_clicked, en IRQ_FALLING car la pin du button1 est en PULL_UP

print('prog start')
run_state(current_state)
while True: # boucle de gestion des inputs et des transitions associées
    try:
        if transitions() is not None: # vérifie s'il y a des nouvelles transitions
            run_state(current_state) # s'il y a eu un changement d'état, l'exécute
        # TODO : demander comment gérer autrement le KeyboardInterrupt ?
        time.sleep(wait_seconds)
    except KeyboardInterrupt: # Ctrl-C
        break

print('prog end')
led.off()