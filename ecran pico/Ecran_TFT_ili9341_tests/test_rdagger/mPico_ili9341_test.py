"""
Raspperry Pi Pico exercise display on ili9341 SPI Display
using rdagger/micropython-ili9341,
MicroPython ILI9341 Display and XPT2046 Touch Screen Drivers
https://github.com/rdagger/micropython-ili9341
"""
from machine import Pin, SPI
from sys import implementation
from os import uname
import utime

import ili9341
from xglcd_font import XglcdFont

import mySetup

print(implementation.name)
print(uname()[3])
print(uname()[4])

print(SPI(0))
print(SPI(1))

display = mySetup.createMyDisplay()

print('Loading fonts...')
print('Loading unispace')
#unispace = XglcdFont('fonts/Unispace12x24.c', 12, 24)
unispace = XglcdFont('Unispace12x24.c', 12, 24)

display.draw_text(0, 0, ili9341.__name__, unispace,
                  ili9341.color565(255, 128, 0))
display.draw_text(0, 25, ili9341.implementation.name, unispace,
                  ili9341.color565(0, 0, 200))
display.draw_text(0, 50, str(ili9341.implementation.version), unispace,
                  ili9341.color565(0, 0, 200))

display.draw_text(0, 100, "https://github.com/", unispace,
                  ili9341.color565(200, 200, 200))
display.draw_text(0, 125, "rdagger/micropython-ili9341", unispace,
                  ili9341.color565(200, 200, 200))

display.draw_text(0, 175, "ABCDEFGHIJKLMNOPQRS", unispace,
                  ili9341.color565(200, 200, 200))
display.draw_text(0, 200, "TUVWXYZ", unispace,
                  ili9341.color565(200, 200, 200))
display.draw_text(0, 225, "abcdefghijklmnopqrs", unispace,
                  ili9341.color565(200, 200, 200))
display.draw_text(0, 250, "tuvwxyz", unispace,
                  ili9341.color565(200, 200, 200))
display.draw_text(0, 275, "01234567890", unispace,
                  ili9341.color565(200, 200, 200))
display.draw_text(0, 300, "~!@#$%^&*()_+`-={}[]", unispace,
                  ili9341.color565(200, 200, 200))
#display.draw_text(0, 325, "\|;:'<>,.?/", unispace,
#                  ili9341.color565(200, 200, 200))
    
for i in range(320):
    display.scroll(i)
    utime.sleep(0.02)
    
for i in range(320, 0, -1):
    display.scroll(i)
    utime.sleep(0.02)

utime.sleep(0.5)
# Display inversion on
display.write_cmd(display.INVON)
utime.sleep(2)
# Display inversion off
display.write_cmd(display.INVOFF)

#while True:
#    pass

display.cleanup()
print("- bye -")