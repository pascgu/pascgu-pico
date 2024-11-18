''' fsm3.2 : idem fsm3 juste au lieu d'avoir les fonctions run_state(),enter_state() et leave_state() qui gèrent plusieurs états, on met ces
    fonctions dans chaque état qui gère eux-même leur propre version.
    PG: je n'aime pas cette version par rapport à fsm3, c'est trop compliqué.
        En plus j'ai essayé de mettre aussi les transitions() mais impossible à cause des définitions
        circulaires, on ne peut pas aller à l'état 2 tant que la classe n'est pas définit et on est justement en train d'écrire la classe 1.

    exemple de machine à état avec 1 bouton et 1 led. 6 états : Off1/On1/On2/Clignotte1/Clignotte2/Off2. Transitions: Off1->bt1 up->On1->bt1 down->On2->bt1 up->Clignotte1->bt1 down->Clignotte2->bt1 up->Off2->bt1 down->Off1
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
clignotte_seconds = 0.3
# vu qu'on fait clignoter plus lentement que les boucles de refresh, pour certaines boucles on ne fera rien et on calcule combien de boucle on changera la LED :
nb_clignotte_counter = clignotte_seconds / wait_seconds

class SState():
    val:int
    fsm:'Fsm'
    def __str__(self) -> str:
        return f"{self.__class__.__name__}#{self.val}"
    def run(self) -> None:
        '''fonction qui exécute l'état'''
        raise NotImplementedError() # à implémenter dans chaque sous-classe
    def enter(self) -> None:
        '''point d'entrée où on peut exécuter des choses quand on entre dans l'état'''
        pass
    def leave(self) -> None:
        '''point d'entrée où on peut exécuter des choses quand on sort de l'état'''
        pass
class StateOff(SState):
    def run(self): led.value(False)
class StateOn(SState):
    def run(self): led.value(True)
class StateClignotte(SState):
    def run(self):
        global nb_clignotte_counter, current_led_value, clignotte_counter
        clignotte_counter += 1
        if clignotte_counter >= nb_clignotte_counter:
            current_led_value = not current_led_value
            led.value(current_led_value)
            clignotte_counter = 0
class StateOff1(StateOff):  val = 1
class StateOff2(StateOff):  val = 6
class StateOn1(StateOn):    val = 2
class StateOn2(StateOn):    val = 3
class StateClignotte1(StateClignotte):
    val = 4
    def enter(self):
        global nb_clignotte_counter, current_led_value, clignotte_counter
        current_led_value = False
        clignotte_counter = 0
class StateClignotte2(StateClignotte):
    val = 5
    def leave(self):
        global current_led_value
        current_led_value = False
        led.value(current_led_value)

# Cette classe n'est là que pour clarifier l'utilisation des états et se rapprocher d'un enum (qui n'existe pas en micropython)
class State():
    Off1        = StateOff1()
    On1         = StateOn1()
    On2         = StateOn2()
    Clignotte1  = StateClignotte1()
    Clignotte2  = StateClignotte2()
    Off2        = StateOff2()
    @classmethod
    def set_fsm(cls, fsm:'Fsm'):
        cls.Off1.fsm = cls.On1.fsm = cls.On2.fsm = cls.Clignotte1.fsm = cls.Clignotte2.fsm = \
            cls.Off2.fsm = fsm

class Fsm():
    current_state:SState = State.Off1 # init
    def run_state(self):
        self.current_state.run()
    def change_state(self, state:SState):
        '''fonction qui réalise le changement d'état.
            Cette fonction n'a pas beaucoup d'intérêt sauf pour réaliser des opérations quand on entre ou qu'on quitte un état
        '''
        if self.current_state != state:
            self.current_state.leave() # avant de changer, on quitte l'ancien état

            # change l'état
            print(f"change d'etat de {self.current_state} -> {state}")
            self.current_state = state
            
            state.enter() # après avoir changé, on entre dans le nouvel état

    def transitions(self):
        '''fonction qui teste s'il y a des transitions déclenchées et si c'est le cas change d'état'''
        bt1_pressed = not button1.value() # car PULL_UP, défaut 1 et si enfoncé 0
        new_state = None
        if self.current_state == State.Off1:
            if bt1_pressed: new_state = State.On1
        elif self.current_state == State.On1:
            if not bt1_pressed: new_state = State.On2
        elif self.current_state == State.On2:
            if bt1_pressed: new_state = State.Clignotte1
        elif self.current_state == State.Clignotte1:
            if not bt1_pressed: new_state = State.Clignotte2
        elif self.current_state == State.Clignotte2:
            if bt1_pressed: new_state = State.Off2
        elif self.current_state == State.Off2:
            if not bt1_pressed: new_state = State.Off1
        
        if new_state != None:
            self.change_state(new_state)

fsm = Fsm()
State.set_fsm(fsm)

############### MAIN #################

current_led_value = False
clignotte_counter = 0
print('prog start')
while True:
    try:
        fsm.run_state()     # refresh l'état en cours
        fsm.transitions()   # vérifie s'il y a des transitions
        sleep(wait_seconds)
    except KeyboardInterrupt: # Ctrl-C
        break

print('prog end')
led.off()