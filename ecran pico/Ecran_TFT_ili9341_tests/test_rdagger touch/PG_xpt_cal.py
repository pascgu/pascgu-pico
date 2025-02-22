from machine import Pin, SPI
from sys import implementation
from os import uname
import ili9341
from xglcd_font import XglcdFont
import gt911
import mySetupX
from utime import sleep

print(implementation.name) # type: ignore
print(uname()[3])
print(uname()[4])

print(SPI(0))
print(SPI(1))

minX = maxX = minY = maxY = 500

def on_touch(pin_interrupt):
    global gt911Touch
    #global minX, maxX, minY, maxY
    
    points = gt911Touch.get_points()
    if points:
        print("Received touch events:")
        for i, point in enumerate(points):
            print(f"  Touch {i+1}: {point.x}, {point.y}, size: {point.size}")
            #display.fill_circle(point.x, point.y, 2, ili9341.color565(0, 255, 0))
            display.fill_circle(point.y, 320-point.x, 2, ili9341.color565(0, 255, 0))
    #touchXY = gt911Touch.get_touch()
    #rawX = gt911Touch.send_command(gt911Touch.GET_X)
    #rawY = gt911Touch.send_command(gt911Touch.GET_Y)
    
    # if rawX != 0:
    #     if rawX > maxX:
    #         maxX = rawX
    #     elif rawX < minX:
    #         minX = rawX
    # if rawY != 0:    
    #     if rawY > maxY:
    #         maxY = rawY
    #     elif rawY < minY:
    #         minY = rawY
    
    # display.fill_circle(x, y, 2, ili9341.color565(0, 255, 0))
    # print(str(x) + ":" + str(y) + " / " + str(rawX) + ":" + str(rawY))
    
    # if touchXY != None:
    #     # touchX = touchXY[0]
    #     # touchY = touchXY[1]
    #     touchX = touchXY.x
    #     touchY = touchXY.y
    #     display.fill_circle(touchX, touchY, 2, ili9341.color565(255, 0, 0))
    #     print(str(touchX) + ":" + str(touchY))
        
    # xReading = "X: " + str(minX) + " - " + str(maxX) + "       "
    # yReading = "Y: " + str(minY) + " - " + str(maxY) + "       "
        
    # display.draw_text(0, 100, xReading, unispace,
    #               ili9341.color565(255, 128, 0))
    # display.draw_text(0, 125, yReading, unispace,
    #               ili9341.color565(255, 128, 0))

display = mySetupX.createMyDisplay()
#xptTouch = mySetupX.createXPT(xpt_touch)
gt911Touch = mySetupX.createTouch(on_touch)

print('Loading fonts...')
print('Loading unispace')
#unispace = XglcdFont('fonts/Unispace12x24.c', 12, 24)
unispace = XglcdFont('Unispace12x24.c', 12, 24)

display.draw_text(0, 0, ili9341.__name__, unispace,
                  ili9341.color565(255, 128, 0))
display.draw_text(0, 25, ili9341.implementation.name, unispace, # type: ignore
                  ili9341.color565(0, 0, 200))
display.draw_text(0, 50, str(ili9341.implementation.version), unispace, # type: ignore
                  ili9341.color565(0, 0, 200))

try:
    while True:
        sleep(0.01)
except KeyboardInterrupt:
    pass

display.cleanup()
print("- bye -")