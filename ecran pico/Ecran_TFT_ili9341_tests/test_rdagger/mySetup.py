from ili9341 import Display
from machine import Pin, SPI

TFT_CLK_PIN = const(2)
TFT_MOSI_PIN = const(3)
TFT_MISO_PIN = const(4)

TFT_CS_PIN = const(5)
TFT_RST_PIN = const(7)
TFT_DC_PIN = const(6)

def createMyDisplay():
    #spi = SPI(0, baudrate=40000000, sck=Pin(TFT_CLK_PIN), mosi=Pin(TFT_MOSI_PIN))
    #spiTFT = SPI(0, baudrate=51200000, sck=Pin(TFT_CLK_PIN), mosi=Pin(TFT_MOSI_PIN))
    #spiTFT = SPI(0, baudrate=10000000, sck=Pin(TFT_CLK_PIN), mosi=Pin(TFT_MOSI_PIN))
    spiTFT = SPI(0, baudrate=40000000, sck=Pin(TFT_CLK_PIN), mosi=Pin(TFT_MOSI_PIN))
    #spiTFT = SPI(0, baudrate=10000000, sck=Pin(TFT_CLK_PIN), mosi=Pin(TFT_MOSI_PIN), miso=Pin(TFT_MISO_PIN))
    #spiTFT = SPI(0, baudrate=10000000, sck=Pin(TFT_CLK_PIN), miso=Pin(TFT_MISO_PIN))
    #display = Display(spiTFT, dc=Pin(TFT_DC_PIN), cs=Pin(TFT_CS_PIN), rst=Pin(TFT_RST_PIN))
    # display = Display(spiTFT, dc=Pin(TFT_DC_PIN), cs=Pin(TFT_CS_PIN), rst=Pin(TFT_RST_PIN), width=320, height=480) # marche vertical
    display = Display(spiTFT, dc=Pin(TFT_DC_PIN), cs=Pin(TFT_CS_PIN), rst=Pin(TFT_RST_PIN), width=480, height=320, rotation=270) # marche
    #display.invert(True) # pour une raison étrange, les couleurs de cette lib sont inversées sur cet écran => 26-01-2025 retiré car créer img2rgb565inv.py qui le fait
    display.invert(True) # 31-01-2025 : remis car c'est tout l'écran qui utilise les couleurs inversées par rapport à la lib ili9341
    return display