
from ucollections import namedtuple
import ili9341
from machine import Pin, SPI
from picoTFT_drivers import GT911_picoTFT

Rect = namedtuple("Rect", ["x", "y", "w", "h"])

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

    def __init__(self, touch_handler, use_time_for_touch=False, rotation=270):
        self.display = self.create_display(rotation)
        self.touch = self.create_touch(touch_handler, use_time_for_touch)

    def create_display(self, rotation=270):
        spiTFT = SPI(0, baudrate=62_500_000, sck=Pin(self.TFT_CLK_PIN), mosi=Pin(self.TFT_MOSI_PIN))
        self.rotation = rotation
        if rotation==90 or rotation==270:
            self.width = 480
            self.height = 320
        else: # vertical
            self.width = 320
            self.height = 480
        display = ili9341.Display(spiTFT, dc=Pin(self.TFT_DC_PIN), cs=Pin(self.TFT_CS_PIN), rst=Pin(self.TFT_RST_PIN),
                                  width=self.width, height=self.height, rotation=self.rotation)
        display.invert(True) # l'écran gère les couleurs de façon inversée (bits) par rapport à la lib ili9341.
        self.default_invert=True
        return display

    def create_touch(self, touch_handler=None, use_time=False):
        tp = GT911_picoTFT(sda=self.TOUCH_I2C_SDA_PIN, scl=self.TOUCH_I2C_SCL_PIN,
                           interrupt=self.TOUCH_INT_PIN, reset=self.TOUCH_RESET_PIN,
                           width=self.width, height=self.height, rotation=self.rotation,
                           use_time=use_time, freq=100_000)
        tp.begin()
        tp.enable_interrupt(self.on_touch_interrupt)
        self.touch_handler = touch_handler
        return tp
    
    def on_touch_interrupt(self, pin_interrup):
        self.touch.get_points()
        # attention touch.buff_points est un buffer pré-alloué de TouchPt.
        # Pour pouvoir allouer de la mémoire, utiliser micropython.schedule et bien penser
        #  à faire buff_points[i].clone() pour créer un nouvel objet et pas ceux du buffer buff_points.
        if self.touch_handler:
            self.touch_handler(self.touch.buff_points, self.touch.buff_points_len)
    
    def disable_interrupt(self):
        self.touch.disable_interrupt()
    def enable_interrupt(self):
        self.touch.enable_interrupt(self.on_touch_interrupt)

    def cleanup(self):
        self.display.cleanup()
    
    def clear(self, color:int=0):
        self.display.clear(color)
    
    def center_for_text(self, rect:Rect, txt:str, fontSize:tuple=(8,8)):
        x = int(rect.x + rect.w/2 - len(txt)*fontSize[0]/2)
        y = int(rect.y + rect.h/2 - 1*fontSize[1]/2)
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
