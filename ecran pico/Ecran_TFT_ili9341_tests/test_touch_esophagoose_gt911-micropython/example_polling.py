import micropython

import gt911
import gt911_constants as gt

micropython.alloc_emergency_exception_buf(100)


tp = gt911.GT911(sda=8, scl=9, interrupt=11, reset=10)
# suite test avec scanner : 0x5d (=93=gt.Addr.ADDR1)
tp.begin(gt.Addr.ADDR1)
print(f"Finished initialization.")
print(f"  Screen: {tp.width}x{tp.height}")


while True:
    points = tp.get_points()
    if points:
        print("Received touch events:")
        for i, point in enumerate(points):
            print(f"  Touch {i+1}: {point.x}, {point.y}, size: {point.size}")
