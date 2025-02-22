
from ucollections import deque
from colors import *
from picoTFT_drivers import TouchPt
from picoTFTwTouch import *
from picoTFT_Control import *

''' PG : Classe permettant de gérer à la fois l'affichage et le Touch de
         l'écran de S2Pi "TFT Pico Breadboard Kit Plus w/ Capacitive Touch".
    PG : Cette classe héritée permet de gérer en plus une UI avec des boutons.
'''
class picoTFT_UI(picoTFTwTouch):
    def __init__(self, touch_handler=None, use_time_for_touch=True, rotation=270, deque_maxlen=1000):
        super().__init__(touch_handler, use_time_for_touch=use_time_for_touch, rotation=rotation)
        self.controls:list[Control] = []
        self.ctrls_touched:deque[tuple[Control,bool]] = deque((), deque_maxlen)
        #self.ctrls_touched_last_time = {}
        self.ctrls_touched_in_interrupt:deque[Control] = deque((), deque_maxlen)
        self.ctrls_touched_last_interrupt:deque[Control] = deque((), deque_maxlen)

    def on_touch_interrupt(self, pin_interrup):
        # cette fonction est appelée environ tous les 10_000us au mieux si on laisse appuyé
        # si on relève le doigt, il y a 3 interrupts déclenchés avec 0 point
        self.touch.get_points()
        p_i = 0
        while self.ctrls_touched_in_interrupt: # == clear()
            self.ctrls_touched_in_interrupt.popleft()
        while p_i < self.touch.buff_points_len:
            pt:TouchPt = self.touch.buff_points[p_i]
            for c_i in range(len(self.controls)-1, -1, -1): # parcourt inversé: besoin car les boutons de la fin sont + près (z-offset) et doivent obtenir le clic
                ctrl = self.controls[c_i]
                if ctrl.hit_test(pt.x, pt.y):
                    last_touched = ctrl in self.ctrls_touched_last_interrupt
                    self.ctrls_touched_in_interrupt.append(ctrl)
                    ctrl.on_touch_callback_interrupt(last_touched)
                    ctrls_touched_countains_ctrl=[True for c,lt in self.ctrls_touched if c==ctrl] # équivalent à : ctrl in ctrls_touched
                    if not ctrls_touched_countains_ctrl:
                        self.ctrls_touched.append((ctrl,last_touched))
                    self.touch.remove_point(p_i)
                    p_i -= 1
                    break
            p_i += 1
        
        if self.touch.buff_points_len:
            if self.touch_handler is not None:
                self.touch_handler(self.touch.buff_points, self.touch.buff_points_len)
        
        while self.ctrls_touched_last_interrupt: # == clear()
            self.ctrls_touched_last_interrupt.popleft()
        while self.ctrls_touched_in_interrupt:
            ctrl:Control = self.ctrls_touched_in_interrupt.popleft()
            self.ctrls_touched_last_interrupt.append(ctrl)
    
    def add_control(self, ctrl):
        self.controls.append(ctrl)
        #self.ctrls_touched_last_time[ctrl] = 0
    def add_controls(self, ctrls:list):
        for i in range(len(ctrls)):
            self.add_control(ctrls[i])
    
    def draw_controls(self):
        for i in range(len(self.controls)):
            ctrl = self.controls[i]
            ctrl.draw(self)
    
    def redraw(self, color:int=0):
        self.clear(color)
        self.draw_controls()
    
    def manage_ctrls_callback(self):
        # Cette fonction est exécutée en moyenne tous les 400us (=0.4ms) si pas de bouton appuyé. Si 1 bouton: 7400 (si ctrl.on_touch_callback) ou 500 (sinon)
        # Elle est donc appelée bien plus souvent que les interrupt (env 10_000us eux)
        while len(self.ctrls_touched)>0:
            ctrl,last_touched = self.ctrls_touched.popleft()
            ctrl.on_touch_callback(last_touched)
