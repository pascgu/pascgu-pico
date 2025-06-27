
from colors import *
from picoTFTwTouch import *
from machine import Timer
from micropython import schedule

class CtrlTimer():
    def __init__(self, ctrl=None, use_schedule=False, timer:Timer|None=None):
        self.timer = timer or Timer()
        self.ctrl = ctrl
        self.use_schedule = use_schedule

    def wait(self, period_ms, callback):
        self.timer.deinit()
        if self.use_schedule:
            self.timer.init(mode=Timer.ONE_SHOT, period=period_ms, callback=lambda t:schedule(callback,self.ctrl))
        else:
            self.timer.init(mode=Timer.ONE_SHOT, period=period_ms, callback=lambda t:callback(self.ctrl))
        
    def periodic(self, period_ms, callback, freq=-1):
        self.timer.deinit()
        if self.use_schedule:
            self.timer.init(mode=Timer.PERIODIC, period=period_ms, freq=freq, callback=lambda t:schedule(callback,self.ctrl))
        else:
            self.timer.init(mode=Timer.PERIODIC, period=period_ms, freq=freq, callback=lambda t:callback(self.ctrl))

    def stop(self):
        self.timer.deinit()
    
class Control():
    __timer=None
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
    
    def timer(self) -> CtrlTimer:
        if self.__timer is None:
            self.__timer = CtrlTimer(self)
        return self.__timer
    
    def __str__(self):
        return self.name+"<"+type(self).__name__+">"



class Button(Control):
    '''Crée un nouveau bouton. Bien penser à l'ajouter après avec picoTFT_UI.add_button (ou add_buttons).

        Args:
            name: nom du control
            rect (Rect): Coordonnées x,y,w,h du bouton
            callback (lambda bt): Fonction appelée lorsqu'un des boutons a été appuyé. Cette fonction
                                    sera appelée par picoTFT_UI.manage_ctrls_callback() qui sera faite dans
                                    le "while True" principal, là où on a le temps de faire + de choses.
            callback_interrupt (lambda bt): Fonction appelée immédiatement par l'interruption de l'irq. Dans
                                            ces fonctions d'interrupt, il faut le min d'allocation mémoire et
                                            d'actions, celles-ci devront être faite dans callback.
            label (str): Nom du bouton qui sera affiché au milieu. Default=""
            foreColor: couleur du texte du label
            backColor: couleur de fond du bouton
            autoclick: mettre à True permet de lancer plusieurs fois le callback tant qu'on appuie sur le bouton.
                        Si False, ça ne le déclenche qu'une fois.
    '''
    def __init__(self, name:str, rect:Rect, callback, callback_interrupt=None,
                 label:str="", foreColor=black, backColor=color565x(0x1CB7BC),
                 autoclick=False):
        super().__init__(name, callback, callback_interrupt)
        self.rect:Rect = rect
        self.label:str = label
        self.foreColor = foreColor
        self.backColor = backColor
        self.autoclick = autoclick
    
    def draw(self, TFT:picoTFTwTouch):
        TFT.fill_rounded_rect(self.rect,self.backColor)
        if self.label:
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
