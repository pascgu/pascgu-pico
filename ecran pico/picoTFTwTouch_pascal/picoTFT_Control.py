
from colors import *
from picoTFTwTouch import *

class Control():
    def __init__(self, name:str, callback, callback_interrupt=None):
        self.name = name
        self.callback = callback
        self.callback_interrupt = callback_interrupt

    def hit_test(self, x, y) -> bool:
        raise NotImplementedError()
    
    def draw(self, TFT:picoTFTwTouch):
        raise NotImplementedError()

    def on_touch_callback_interrupt(self, last_touched=False):
        if self.callback_interrupt != None:
            self.callback_interrupt(self)

    def on_touch_callback(self, last_touched=False):
        if self.callback != None:
            self.callback(self)
    
    def __str__(self):
        return self.name+"<"+type(self).__name__+">"
        

class Button(Control):
    '''Crée un nouveau bouton. Bien penser à l'ajouter après avec picoTFT_UI.add_button (ou add_buttons).

        Args:
            name: nom du control
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
    def __init__(self, name:str, rect:Rect, label:str, callback, callback_interrupt=None,
                 foreColor=black, backColor=color565x(0x1CB7BC),
                 autoclick=False):
        super().__init__(name, callback, callback_interrupt)
        self.rect = rect
        self.label = label
        self.foreColor = foreColor
        self.backColor = backColor
        self.autoclick = autoclick
    
    def draw(self, TFT:picoTFTwTouch):
        TFT.fill_rounded_rect(self.rect,self.backColor)
        TFT.draw_text8x8_centered(self.rect, self.label, self.foreColor, background=self.backColor)
    
    def hit_test(self, x, y) -> bool:
        insideX = x >= self.rect.x and x <= self.rect.x+self.rect.w
        insideY = y >= self.rect.y and y <= self.rect.y+self.rect.h
        return insideX and insideY
    
    def on_touch_callback_interrupt(self, last_touched=False):
        if not last_touched or self.autoclick:
            super().on_touch_callback_interrupt(last_touched)
    
    def on_touch_callback(self, last_touched=False):
        if not last_touched or self.autoclick:
            #super().on_touch_callback(last_touched) # fait dans on_click()
            self.on_click()

    def on_click(self):
        # appelle le callback associé à ce bouton quand il y a un nouveau clic
        super().on_touch_callback()
