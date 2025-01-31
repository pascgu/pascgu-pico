
from collections import namedtuple
import utime
import ili9341
from machine import Pin, SPI
import gt911
import gt911_constants as gt
from colors import *
from picoTFTwTouch import *

''' PG : Classe permettant de gérer à la fois l'affichage et le Touch de
         l'écran de S2Pi "TFT Pico Breadboard Kit Plus w/ Capacitive Touch".
    PG : Cette surcharge permet de gérer une UI avec des boutons
'''
class picoTFT_UI(picoTFTwTouch):
    def __init__(self, touch_handler, horizontal=True):
        super().__init__(touch_handler, horizontal)
        self.buttons = []

    def on_touch(self, pin_interrup):
        points = self.touch.get_points()
        for p_i in range(len(points)-1, -1, -1): # parcourt inversé: besoin si on suppr des points
            pt = points[p_i]
            for b_i in range(len(self.buttons)-1, -1, -1): # parcourt inversé: besoin car les boutons de la fin sont + près (zoffset) et doivent obtenir le clic
                bt = self.buttons[b_i]
                if bt.hit_test(pt.x, pt.y):
                    bt.click()
                    points.remove(pt)
                    break
        self.touch_handler(points)
    
    def add_button(self, bt):
        self.buttons.append(bt)
    def add_buttons(self, bts:list):
        for i in range(len(bts)):
            self.add_button(bts[i])
    
    def draw_buttons(self):
        for i in range(len(self.buttons)):
            bt = self.buttons[i]
            bt.draw(self)
    
    def redraw(self, color:int=0):
        self.clear(color)
        self.draw_buttons()

    def manage_buttons_click(self):
        pass # TODO : faire la gestion des clics de chaque boutons ici
        

class Button():
    minClickDelay=200 # minimum 200ms entre 2 click si on reste appuyé sur le bouton, ça ne doit rien faire
    '''Crée un nouveau bouton. Bien penser à l'ajouter après avec picoTFT_UI.add_button (ou add_buttons).

        Args:
            rect (Rect): Coordonnées x,y,w,h du bouton
            label (str): Nom du bouton qui sera affiché au milieu
            callback (lambda bt): Fonction appelée lorsqu'un des boutons a été appuyé. Cette fonction
                                    sera appelée par picoTFT_UI.manage_buttons_click() qui sera faite dans
                                    le "while True" principal, là où on a le temps de faire + de chose.
            callback_interrupt (lambda bt): 
TODO à compléter. 
                            Bien penser à appeler le Button.on_callback_interrupt dans votre fonction !
            foreColor: couleur du texte du label
            backColor: couleur de fond du bouton
            autoclick: mettre à True permet de lancer plusieurs fois le callback tant qu'on appuie sur le bouton.
                        Si False, ça ne le déclenche qu'une fois.
    '''
    def __init__(self, rect:Rect, label:str, callback, callback_interrupt=None,
                 foreColor=black, backColor=color565x(0x1CB7BC),
                 autoclick=False):
        self.rect = rect
        self.label = label
        self.callback = callback
        self.foreColor = foreColor
        self.backColor = backColor
        if autoclick: self.enable_autoclick()
        else: self.autoclick=False # use enable_autoclick() to enable it
        self.last_click_time = utime.ticks_ms()
        self.callback_interrupt = callback_interrupt
        if callback_interrupt==None: self.callback_interrupt = self.on_callback_interrupt
    
    def draw(self, TFTui: picoTFT_UI):
        TFTui.fill_rounded_rect(self.rect,self.backColor)
        TFTui.draw_text8x8_centered(self.rect, self.label, self.foreColor, background=self.backColor)
    
    def hit_test(self, x, y) -> bool:
        insideX = x >= self.rect.x and x <= self.rect.x+self.rect.w
        insideY = y >= self.rect.y and y <= self.rect.y+self.rect.h
        return insideX and insideY
    
    def enable_autoclick(self, clickDelay=300):
        self.autoclick = True
        self.minClickDelay_save = self.minClickDelay
        self.minClickDelay = clickDelay
    
    def disable_autoclick(self):
        self.autoclick = False
        self.minClickDelay = self.minClickDelay_save

    def on_callback_interrupt(self):
        pass # TODO : finir on_callback_interrupt

    def click(self):
        time = utime.ticks_ms()
        if utime.ticks_diff(time, self.last_click_time) >= self.minClickDelay:
            # on ne déclenche pas le callback tout le temps
            self.callback(self)

            if self.autoclick:
                self.last_click_time = time # on ne remet le timer à 0 que lorsqu'un clic a été lancé
        if not self.autoclick:
            self.last_click_time = time # on remet le timer à 0 à chaque fois qu'on passe dans cette fonction
