import ili9341

def color565(r, g, b):
    return ili9341.color565(r,g,b)
def color565x(hex):
    return color565(hex>>16&0xFF,hex>>8&0xFF,hex&0xFF)

black=color565x(0x000000)
white=color565x(0xFFFFFF)
red=color565x(0xFF0000)
green=color565x(0x00FF00)
blue=color565x(0x0000FF)
cyan=color565x(0x00FFFF)
magenta=color565x(0xFF00FF)
yellow=color565x(0xFFFF00)
orange=color565x(0xFF6A00)
pink=color565x(0xFF3399)
purple=color565x(0x6600FF)
azure=color565x(0x0066CC)
darkgreen=color565x(0x007F00)
brown=color565x(0xA52A2A)
lightgrey=color565x(0xC0C0C0)
grey=color565x(0x808080)
darkgrey=color565x(0x606060)