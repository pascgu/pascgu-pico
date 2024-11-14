''' fsm1 : exemple de machine à état avec 2 boutons et 1 led. 3 états : Off/On/Clignotte. Transitions: Off->bt1->On->bt1->Off  On|Off->bt2->Clignotte->bt1->Off
    C'est plus clair avec le fichier fsm1-drawio.png qui peut être ouvert comme une image ou avec le logiciel DrawIO et qui permet de créer ces diagrammes.
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
button2 = Pin(16, Pin.IN, Pin.PULL_DOWN) # Pin.PULL_DOWN indique que l'on veut que cette pin soit relié au Ground (GND) et une résistance de 10 ohm. L'autre patte du bouton doit être relié à 3V3(OUT).
led = Pin(12, Pin.OUT)
wait_seconds = 0.5 # délai entre 2 boucles de refresh des états et test des transitions

class State():
    Off = 1
    On = 2
    Clignotte = 3

def run_state(state):
    '''fonction qui exécute l'état'''
    global current_led_value, led
    if state == State.Off:
        led.value(False)
    elif state == State.On:
        led.value(True)
        # Note : au lieu de faire un appel qui change la LED à chaque boucle, on aurait pu ne la changer qu'à l'entrée dans cet état et à la sortie de cet état
    elif state == State.Clignotte:
        current_led_value = not current_led_value
        led.value(current_led_value)

def change_state(state):
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

def enter_state(state):
    '''point d'entrée où on peut exécuter des choses quand on entre dans l'état'''
    global current_led_value, led
    if state == State.Clignotte: # init l'état Clignotte
        current_led_value = False
        led.value(current_led_value)
def leave_state(state):
    '''point d'entrée où on peut exécuter des choses quand on sort de l'état'''
    global led
    if state == State.Clignotte:
        led.value(False) # remet la led à éteinte, parce que pourquoi pas

def transitions():
    '''fonction qui teste s'il y a des transitions déclenchées et si c'est le cas change d'état'''
    global current_state
    bt1_new_pressed = is_bt1_new_pressed()
    bt2_new_pressed = is_bt2_new_pressed()
    new_state = None
    if current_state == State.Off:
        if bt1_new_pressed: new_state = State.On
        if bt2_new_pressed: new_state = State.Clignotte
    elif current_state == State.On:
        if bt1_new_pressed: new_state = State.Off
        if bt2_new_pressed: new_state = State.Clignotte
    elif current_state == State.Clignotte:
        if bt1_new_pressed: new_state = State.Off
    
    if new_state != None:
        change_state(new_state)

bt1_last_pressed=False
def is_bt1_new_pressed():
    '''fonction permettant juste de savoir si le bouton vient à l'instant d'être enfoncé (et ignore les cas où il était déjà enfoncé avant)'''
    global button1, bt1_last_pressed
    bt1_pressed=not button1.value() # car PULL_UP, défaut 1 et si enfoncé 0
    ret=False
    if bt1_pressed and not bt1_last_pressed:
        ret=True
    bt1_last_pressed=bt1_pressed
    return ret

bt2_last_pressed=False
def is_bt2_new_pressed():
    '''fonction permettant juste de savoir si le bouton vient à l'instant d'être enfoncé (et ignore les cas où il était déjà enfoncé avant)'''
    global button2, bt2_last_pressed
    bt2_pressed=button2.value() # car PULL_DOWN, defaut 0 et si enfoncé 1
    ret=False
    if bt2_pressed and not bt2_last_pressed:
        ret=True
    bt2_last_pressed=bt2_pressed
    return ret


############### MAIN #################

current_state=State.Off # init
current_led_value=False
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