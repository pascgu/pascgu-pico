
from collections import namedtuple
import utime
import ili9341
from machine import Pin, SPI
import gt911
import gt911_constants as gt

Rect = namedtuple("Rect", ["x", "y", "w", "h"])
TouchPt = namedtuple("TouchPt", ["id", "x", "y", "size","t"])

class GT911V(gt911.GT911):
    def __init__(self, sda, scl, interrupt, reset, display_height, use_time=False, freq=100_000):
        super().__init__(sda, scl, interrupt, reset, freq)
        self.display_height = display_height
        self.use_time = use_time
    
    def get_points(self):
        points = []
        info = self.read(gt.POINT_INFO, 1)[0]
        ready = bool((info >> 7) & 1)
        # large_touch = bool((info >> 6) & 1)
        touch_count = info & 0xF
        if ready and touch_count > 0:
            ticks_us = 0
            if self.use_time: ticks_us = utime.ticks_us()
            for i in range(touch_count):
                data = self.read(gt.POINT_1 + (i * 8), 7)
                points.append(self.parse_point(data, ticks_us))
        self.write(gt.POINT_INFO, [0])
        return points
    
    def parse_point(self, data, ticks_us):
        track_id = data[0]
        x = data[1] + (data[2] << 8)
        y = data[3] + (data[4] << 8)
        size = data[5] + (data[6] << 8)
        return TouchPt(track_id, x, y, size, ticks_us)
    
'''GT911 with management of horizontal points instead of vertical'''
class GT911H(GT911V):
    def __init__(self, sda, scl, interrupt, reset, display_height, use_time=False, freq=100_000):
        super().__init__(sda, scl, interrupt, reset, display_height, use_time, freq)

    def parse_point(self, data, ticks_us):
        track_id = data[0]
        #x = data[1] + (data[2] << 8)
        #y = data[3] + (data[4] << 8)
        # PG: on inverse les coordonnées si mode horizontal au lieu vertical
        # PG: on est obligé de réécrire cette fonction car c'est elle qui crée les
        #     TouchPoint qui sont des namestuple immutable (donc non modifiables).
        y = self.display_height - (data[1] + (data[2] << 8))
        x = data[3] + (data[4] << 8)
        size = data[5] + (data[6] << 8)
        return TouchPt(track_id, x, y, size, ticks_us)


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

    def __init__(self, touch_handler, use_time_for_touch=False, horizontal=True):
        self.display = self.create_display(horizontal)
        self.touch = self.create_touch(touch_handler, use_time_for_touch, horizontal)

    def create_display(self, horizontal=True):
        spiTFT = SPI(0, baudrate=62_500_000, sck=Pin(self.TFT_CLK_PIN), mosi=Pin(self.TFT_MOSI_PIN))
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

    def create_touch(self, touch_handler=None, use_time=False, horizontal=True):
        if horizontal:
            tp = GT911H(sda=self.TOUCH_I2C_SDA_PIN, scl=self.TOUCH_I2C_SCL_PIN,
                        interrupt=self.TOUCH_INT_PIN, reset=self.TOUCH_RESET_PIN,
                        display_height=self.height, use_time=use_time, freq=100_000)
        else:
            #tp = gt911.GT911(sda=self.TOUCH_I2C_SDA_PIN, scl=self.TOUCH_I2C_SCL_PIN,
            #                 interrupt=self.TOUCH_INT_PIN, reset=self.TOUCH_RESET_PIN)
            
            tp = GT911V(sda=self.TOUCH_I2C_SDA_PIN, scl=self.TOUCH_I2C_SCL_PIN,
                        interrupt=self.TOUCH_INT_PIN, reset=self.TOUCH_RESET_PIN,
                        display_height=self.height, use_time=use_time, freq=100_000)
        tp.begin(gt.Addr.ADDR1)
        if touch_handler!=None:
            tp.enable_interrupt(self.on_touch_interrupt)
            self.touch_handler = touch_handler
        return tp
    
    def on_touch_interrupt(self, pin_interrup):
        points = self.touch.get_points()
        self.touch_handler(points)
    
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
