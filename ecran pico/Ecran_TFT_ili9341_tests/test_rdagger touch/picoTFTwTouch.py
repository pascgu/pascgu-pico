
from collections import namedtuple
import utime
import ili9341
from machine import Pin, SPI
import gt911
import gt911_constants as gt
from colors import *

Rect = namedtuple("Rect", ["x", "y", "w", "h"])

'''GT911 with management of horizontal points instead of vertical'''
class GT911H(gt911.GT911):
    def __init__(self, sda, scl, interrupt, reset, display_height, freq=100_000):
        super().__init__(sda, scl, interrupt, reset, freq)
        self.display_height = display_height

    def parse_point(self, data):
        track_id = data[0]
        #x = data[1] + (data[2] << 8)
        #y = data[3] + (data[4] << 8)
        # PG: on inverse les coordonnées si mode horizontal au lieu vertical
        # PG: on est obligé de réécrire cette fonction car c'est elle qui crée les
        #     TouchPoint qui sont des namestuple immutable (donc non modifiables).
        y = self.display_height - (data[1] + (data[2] << 8))
        x = data[3] + (data[4] << 8)
        size = data[5] + (data[6] << 8)
        return gt911.TouchPoint(track_id, x, y, size)


''' PG : Classe permettant de gérer à la fois l'affichage et le Touch de
         l'écran de S2Pi "TFT Pico Breadboard Kit Plus w/ Capacitive Touch".
'''
class picoTFTwTouch():
    TFT_CLK_PIN = const(2)
    TFT_MOSI_PIN = const(3)
    TFT_MISO_PIN = const(4)

    TFT_CS_PIN = const(5)
    TFT_RST_PIN = const(7)
    TFT_DC_PIN = const(6)

    TOUCH_I2C_SDA_PIN = const(8)
    TOUCH_I2C_SCL_PIN = const(9)

    TOUCH_RESET_PIN = const(10) # TPRST reset
    TOUCH_INT_PIN = const(11) # TPINT interrupt

    def __init__(self, touch_handler, horizontal=True):
        self.display = self.createDisplay(horizontal)
        self.touch = self.createTouch(touch_handler, horizontal)
        self.buttons = []

    def createDisplay(self, horizontal=True):
        spiTFT = SPI(0, baudrate=40000000, sck=Pin(self.TFT_CLK_PIN), mosi=Pin(self.TFT_MOSI_PIN))
        if horizontal:
            self.width = 480
            self.height = 320
            self.rotation = 270
        else: # vertical
            self.width = 320
            self.height = 480
            self.rotation = 0
        display = ili9341.Display(spiTFT, dc=Pin(self.TFT_DC_PIN), cs=Pin(self.TFT_CS_PIN), rst=Pin(self.TFT_RST_PIN),
                                  width=self.width, height=self.height, rotation=self.rotation)
        display.invert(True) # l'écran gère les couleurs de façon inversée (bits) par rapport à la lib ili9341.
        self.default_invert=True
        return display

    def createTouch(self, touch_handler, horizontal=True):
        if horizontal:
            tp = GT911H(sda=self.TOUCH_I2C_SDA_PIN, scl=self.TOUCH_I2C_SCL_PIN,
                        interrupt=self.TOUCH_INT_PIN, reset=self.TOUCH_RESET_PIN,
                        display_height=self.height)
        else:
            tp = gt911.GT911(sda=self.TOUCH_I2C_SDA_PIN, scl=self.TOUCH_I2C_SCL_PIN,
                             interrupt=self.TOUCH_INT_PIN, reset=self.TOUCH_RESET_PIN)
        tp.begin(gt.Addr.ADDR1)
        tp.enable_interrupt(self.onTouch)
        self.touch_handler = touch_handler
        return tp
    
    def onTouch(self, pin_interrup):
        points = self.touch.get_points()
        for p_i in range(len(points)-1, -1, -1):
            pt = points[p_i]
            for i in range(len(self.buttons)):
                bt = self.buttons[i]
                if bt.hitTest(pt.x, pt.y):
                    bt.click()
                    points.remove(pt)
                    break
        self.touch_handler(points)
    
    def addButton(self, bt):
        self.buttons.append(bt)
    def addButtons(self, bts:list):
        for i in range(len(list)):
            self.addButton(bts[i])
    
    def draw_buttons(self):
        for i in range(len(self.buttons)):
            bt = self.buttons[i]
            bt.draw(self)
    
    def cleanup(self):
        self.display.cleanup()
    
    def clear(self, color:int=0):
        self.display.clear(color)
    
    def redraw(self, color:int=0):
        self.clear(color)
        self.draw_buttons()
    
    def center_for_text(self, rect:Rect, txt:str, fontSize:tuple=(8,8)):
        lines=[""]
        # lines = txt.splitlines() # TODO : gérer multilignes ?
        x = int(rect.x + rect.w/2 - len(txt)*fontSize[0]/2)
        y = int(rect.y + rect.h/2 - len(lines)*fontSize[1]/2)
        return (x,y)
    
    def draw_text8x8(self, x, y, text:str, color,  background=0, rotate=0):
        self.display.draw_text8x8(x, y, text, color, background, rotate)

    def draw_text8x8_centered(self, rect:Rect, text:str, color,  background=0, rotate=0):
        self.draw_text8x8(*self.center_for_text(rect,text), text, color, background, rotate)

    def fill_rounded_rect(self, rect:Rect, color):
        self.display.draw_hline(rect.x+2, rect.y, rect.w-3, color) # top
        self.display.draw_hline(rect.x+2, rect.y+rect.h, rect.w-3, color) # bottom
        self.display.draw_vline(rect.x, rect.y+2, rect.h-3, color) # left
        self.display.draw_vline(rect.x+rect.w, rect.y+2, rect.h-3, color) # right
        self.display.fill_rectangle(rect.x+1, rect.y+1, rect.w-1, rect.h-1, color) # inside rect
    

class Button():
    minClickDelay=100 # minimum 100ms entre 2 click si on reste appuyé sur le bouton
    autoclick=False # use enable_autoclick() to 
    def __init__(self, rect:Rect, label, callback, foreColor=black, backColor=color565x(0x1CB7BC)):
        self.rect = rect
        self.label = label
        self.callback = callback
        self.foreColor = foreColor
        self.backColor = backColor
        self.last_click_time = utime.ticks_ms()
    
    def draw(self, display):
        display.fill_rounded_rect(self.rect,self.backColor)
        display.draw_text8x8_centered(self.rect, self.label, self.foreColor, background=self.backColor)
    
    def hitTest(self, x, y) -> bool:
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

    def click(self):
        time = utime.ticks_ms()
        if utime.ticks_diff(time, self.last_click_time) >= self.minClickDelay:
            self.callback(self) # on ne déclenche pas le callback tout le temps
            if self.autoclick:
                self.last_click_time = time # on ne remet le timer à 0 que lorsqu'un clic a été lancé
        if not self.autoclick:
            self.last_click_time = time # on remet le timer à 0 à chaque fois qu'on passe dans cette fonction
