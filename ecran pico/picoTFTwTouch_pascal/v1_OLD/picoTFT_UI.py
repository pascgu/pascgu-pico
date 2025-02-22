
from collections import namedtuple
import utime
import ili9341
from machine import Pin, SPI
import gt911
import gt911_constants as gt
from colors import *
from picoTFTwTouch import *
from picoTFT_Control import *

''' PG : Classe permettant de gérer à la fois l'affichage et le Touch de
         l'écran de S2Pi "TFT Pico Breadboard Kit Plus w/ Capacitive Touch".
    PG : Cette classe héritée permet de gérer en plus une UI avec des boutons.
'''
class picoTFT_UI(picoTFTwTouch):
    def __init__(self, touch_handler=None, use_time_for_touch=True, horizontal=True):
        super().__init__(touch_handler, use_time_for_touch=use_time_for_touch, horizontal=horizontal)
        self.controls:list[Control] = []
        self.ctrls_touched:list[tuple[Control,bool]] = []
        self.ctrls_touched_last_interrupt:list[Control] = []
        self.ctrls_touched_last_interrupt2:list[Control] = []

    def on_touch_interrupt(self, pin_interrup):
        # cette fonction est appelée environ tous les 10_000us au mieux si on laisse appuyé
        # si on relève le doigt, il y a 3 interrupts déclenchés avec 0 point
        points = self.touch.get_points()
        ctrls_touched_in_interrupt = []
        for p_i in range(len(points)-1, -1, -1): # parcourt inversé: besoin si on suppr des points
            pt:TouchPt = points[p_i]
            for c_i in range(len(self.controls)-1, -1, -1): # parcourt inversé: besoin car les boutons de la fin sont + près (zoffset) et doivent obtenir le clic
                ctrl = self.controls[c_i]
                if ctrl.hit_test(pt.x, pt.y):
                    last_touched = ctrl in self.ctrls_touched_last_interrupt or ctrl in self.ctrls_touched_last_interrupt2
                    ctrls_touched_in_interrupt.append(ctrl)
                    ctrl.on_touch_callback_interrupt(last_touched)
                    ctrls_touched_countains_ctrl=[True for c,lt in self.ctrls_touched if c==ctrl] # équivalent à : ctrl in ctrls_touched
                    if not ctrls_touched_countains_ctrl:
                        self.ctrls_touched.append((ctrl,last_touched))
                    points.pop(p_i) # remove pt
                    break
        if points:
            if self.touch_handler is not None:
                self.touch_handler(points)
        self.ctrls_touched_last_interrupt2 = self.ctrls_touched_last_interrupt 
        self.ctrls_touched_last_interrupt = ctrls_touched_in_interrupt 
    
    def add_control(self, ctrl):
        self.controls.append(ctrl)
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
            ctrl,last_touched = self.ctrls_touched.pop(0)
            ctrl.on_touch_callback(last_touched)
