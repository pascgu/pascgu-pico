from ili9341 import Display
from machine import Pin, SPI, I2C
#from xpt2046 import Touch
import gt911
import gt911_constants as gt

TFT_CLK_PIN = const(2)
TFT_MOSI_PIN = const(3)
TFT_MISO_PIN = const(4)

TFT_CS_PIN = const(5)
TFT_RST_PIN = const(7)
TFT_DC_PIN = const(6)

#XPT_CLK_PIN = const(10)
#XPT_MOSI_PIN = const(11)
#XPT_MISO_PIN = const(8)

TOUCH_I2C_SDA_PIN = const(8)
TOUCH_I2C_SCL_PIN = const(9)

TOUCH_RESET_PIN = const(10) # TPRST reset
TOUCH_INT_PIN = const(11) # TPINT interrupt

def createMyDisplay():
    #spi = SPI(0, baudrate=40000000, sck=Pin(TFT_CLK_PIN), mosi=Pin(TFT_MOSI_PIN))
    #spiTFT = SPI(0, baudrate=51200000, sck=Pin(TFT_CLK_PIN), mosi=Pin(TFT_MOSI_PIN))
    #spiTFT = SPI(0, baudrate=10000000, sck=Pin(TFT_CLK_PIN), mosi=Pin(TFT_MOSI_PIN))
    spiTFT = SPI(0, baudrate=40000000, sck=Pin(TFT_CLK_PIN), mosi=Pin(TFT_MOSI_PIN))
    #spiTFT = SPI(0, baudrate=10000000, sck=Pin(TFT_CLK_PIN), mosi=Pin(TFT_MOSI_PIN), miso=Pin(TFT_MISO_PIN))
    #spiTFT = SPI(0, baudrate=10000000, sck=Pin(TFT_CLK_PIN), miso=Pin(TFT_MISO_PIN))
    #display = Display(spiTFT, dc=Pin(TFT_DC_PIN), cs=Pin(TFT_CS_PIN), rst=Pin(TFT_RST_PIN))
    #display = Display(spiTFT, dc=Pin(TFT_DC_PIN), cs=Pin(TFT_CS_PIN), rst=Pin(TFT_RST_PIN), width=320, height=480) # marche
    display = Display(spiTFT, dc=Pin(TFT_DC_PIN), cs=Pin(TFT_CS_PIN), rst=Pin(TFT_RST_PIN), width=320, height=480, rotation=270)
    display.invert(True) # pour une raison étrange, les couleurs de cette lib sont inversées sur cet écran
    return display

def createTouch(touch_handler):
    #i2c = I2C(0, sda=Pin(TOUCH_I2C_SDA_PIN), scl=Pin(TOUCH_I2C_SCL_PIN))
    #xpt = Touch(spiXPT, cs=Pin(XPT_CS_PIN), int_pin=Pin(XPT_INT), int_handler=touch_handler)
    #xpt = TouchI2C(i2cXPT, cs=Pin(XPT_CS_PIN), int_pin=Pin(XPT_INT), int_handler=touch_handler)
    #return xpt
    tp = gt911.GT911(sda=TOUCH_I2C_SDA_PIN, scl=TOUCH_I2C_SCL_PIN, interrupt=TOUCH_INT_PIN, reset=TOUCH_RESET_PIN)
    tp.begin(gt.Addr.ADDR1)
    tp.enable_interrupt(touch_handler)
    return tp