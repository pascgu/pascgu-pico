
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
    def __init__(self, touch_handler=None, horizontal=True):
        super().__init__(touch_handler, horizontal)
        self.controls:list[Control] = []
        self.ctrls_touched:list[Control] = []
        self.last_ctrls_touched:list[Control] = []

    def on_touch_interrupt(self, pin_interrup):
        points = self.touch.get_points()
        for p_i in range(len(points)-1, -1, -1): # parcourt inversé: besoin si on suppr des points
            pt = points[p_i]
            for b_i in range(len(self.controls)-1, -1, -1): # parcourt inversé: besoin car les boutons de la fin sont + près (zoffset) et doivent obtenir le clic
                ctrl = self.controls[b_i]
                if ctrl.hit_test(pt.x, pt.y):
                    if not ctrl in self.ctrls_touched:
                        ctrl.on_touch_callback_interrupt(ctrl in self.last_ctrls_touched)
                        self.ctrls_touched.append(ctrl)
                    points.remove(pt)
                    break
        if points:
            self.touch_handler(points)
    
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

    def on_start_manage(self):
        pass
    def on_stop_manage(self):
        self.last_ctrls_touched = self.ctrls_touched
        self.ctrls_touched = []

    def manage_ctrls_callback(self):
        self.on_start_manage()
        for i in range(len(self.ctrls_touched)):
            ctrl = self.ctrls_touched[i]
            ctrl.on_touch_callback(ctrl in self.last_ctrls_touched)
        self.on_stop_manage()
