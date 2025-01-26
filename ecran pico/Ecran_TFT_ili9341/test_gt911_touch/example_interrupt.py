import micropython

import gt911
import gt911_constants as gt

import time

micropython.alloc_emergency_exception_buf(100)


def on_touch(_):
    points = tp.get_points()
    if points:
        print("Received touch events:")
        for i, point in enumerate(points):
            print(f"  Touch {i+1}: {point.x}, {point.y}, size: {point.size}")


tp = gt911.GT911(sda=8, scl=9, interrupt=11, reset=10)
tp.begin(gt.Addr.ADDR1)
print("Finished initialization.")
print(f"  Screen: {tp.width}x{tp.height}")

tp.enable_interrupt(on_touch)

while True:
    try:
        time.sleep(0.1)
    except KeyboardInterrupt:
        break

print("prog end")