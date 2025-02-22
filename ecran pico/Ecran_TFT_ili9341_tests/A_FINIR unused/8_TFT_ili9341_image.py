from time import sleep
from ili9341 import Display
from machine import Pin, SPI


def test():
    """Test code."""
    # Baud rate of 40000000 seems about the max
    #spi = SPI(1, baudrate=10000000, sck=Pin(14), mosi=Pin(15))
    #display = Display(spi, dc=Pin(6), cs=Pin(17), rst=Pin(7))

    #PG: récup de micropython-ili9341
    ## Baud rate of 40000000 seems about the max
    #spi = SPI(1, baudrate=40000000, sck=Pin(14), mosi=Pin(13))
    #display = Display(spi, dc=Pin(4), cs=Pin(16), rst=Pin(17))

    spi = SPI(0, baudrate=10000000, sck=Pin(2), mosi=Pin(3))
    #display = Display(spi, dc=Pin(6), cs=Pin(5), rst=Pin(7), width=320, height=480, rotation=270)
    display = Display(spi, dc=Pin(6), cs=Pin(5), rst=Pin(7), width=320, height=480, rotation=270, bgr=False)

    try:
        #display.draw_image('fruits.raw', 0, 0, 240, 320)
        #def draw_image(self, path, x=0, y=0, w=320, h=240):
        #display.draw_image('./fruits.raw', 0, 0, 320, 400)
        #display.draw_image('./avatar.raw', 0, 0, 120, 120)
        #display.draw_image('./fruits2_480x320.raw', 0, 0, 320, 480)
        display.draw_image('MicroPython128x128.raw', 0, 129, 128, 128)
        sleep(30)
        display.cleanup()
    except Exception as ex:
        display.cleanup()
        raise ex



test()