
from ucollections import deque
from utime import ticks_us, ticks_diff
from micropython import schedule
from colors import *
from picoTFT_drivers import TouchPt
from picoTFTwTouch import *
from picoTFT_Control import *

''' PG : Classe permettant de gérer à la fois l'affichage et le Touch de
         l'écran de S2Pi "TFT Pico Breadboard Kit Plus w/ Capacitive Touch".
    PG : Cette classe héritée permet de gérer en plus une UI avec des boutons.
'''
class picoTFT_UI(picoTFTwTouch):
    def __init__(self, touch_handler=None, use_time_for_touch=True, rotation=270,
                 deque_maxlen=100, touch_point_min_diff_us=50_000):
        super().__init__(touch_handler, use_time_for_touch=use_time_for_touch, rotation=rotation)
        self.touch_point_min_diff_us = touch_point_min_diff_us # 30_000 correspond à 3x on_touch_interrupt ce qui est le min (50k pour être large)
        self.controls:list[Control] = [] # liste des controls ajoutés via add_control()
        self.ctrls_touched:deque[tuple[Control,bool]] = deque((), deque_maxlen) # queue des boutons appuyés
        self.ctrls_touched_last_time:dict[Control,int] = {} # dernière fois que le bouton était appuyé dans un interrupt

    def on_touch_interrupt(self, pin_interrup):
        # cette fonction est appelée environ tous les 10_000us au mieux si on laisse appuyé
        # si on relève le doigt, il y a 3 interrupts déclenchés avec 0 point
        self.touch.get_points()
        #no_pts = self.touch.buff_points_len == 0 # aucun point, on relève le doigt
        p_i = self.touch.buff_points_len-1
        while p_i >= 0:
            pt:TouchPt = self.touch.buff_points[p_i]
            for c_i in range(len(self.controls)-1, -1, -1): # parcourt inversé: besoin car les boutons de la fin sont + près (z-offset) et doivent obtenir le clic
                ctrl = self.controls[c_i]
                if ctrl.hit_test(pt.x, pt.y):
                    diff = ticks_diff(pt.t, self.ctrls_touched_last_time[ctrl])
                    last_touched = diff < self.touch_point_min_diff_us # en dessous de ça, on considère que le bouton était déjà appuyé
                    self.ctrls_touched_last_time[ctrl] = pt.t

                    ctrl.on_touch_callback_interrupt(last_touched)
                    ctrls_touched_countains_ctrl=False
                    for c,lt in self.ctrls_touched: # équivalent à : ctrl in ctrls_touched
                        if c==ctrl:
                            ctrls_touched_countains_ctrl=True
                            break
                    if not ctrls_touched_countains_ctrl:
                        self.ctrls_touched.append((ctrl,last_touched))
                    self.touch.remove_point(p_i)
                    break
            p_i -= 1
        
        #if self.touch.buff_points_len or no_pts:
        if self.touch_handler is not None:
            if self.touch.buff_points_len:
                self.touch_handler(self.touch.buff_points, self.touch.buff_points_len)

    def add_control(self, ctrl):
        self.controls.append(ctrl)
        self.ctrls_touched_last_time[ctrl] = 0
    def add_controls(self, ctrls:list):
        for i in range(len(ctrls)):
            self.add_control(ctrls[i])
    def remove_control(self, ctrl:Control):
        self.controls.remove(ctrl)
        del self.ctrls_touched_last_time[ctrl]
    
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
        if self.ctrls_touched:
            ctrl,last_touched = self.ctrls_touched.popleft()
            ctrl.on_touch_callback(last_touched)


class picoTFT_UI_schedule(picoTFT_UI):
    def __init__(self, touch_handler=None, use_time_for_touch=True, rotation=270,
                 deque_maxlen=100, touch_point_min_diff_us=50_000):
        super().__init__(touch_handler, use_time_for_touch=use_time_for_touch, rotation=rotation,
                         deque_maxlen=deque_maxlen, touch_point_min_diff_us=touch_point_min_diff_us)
    
    def on_touch_interrupt(self, pin_interrup):
        schedule(super().on_touch_interrupt, pin_interrup)