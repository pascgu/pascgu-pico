from colors import *
# import ili9341                #PG: je le laisse aussi pour ne pas oublier de l'upload
# from picoTFTwTouch import *   #PG: je le laisse aussi pour ne pas oublier de l'upload
# import picoTFT_drivers        #PG: je le laisse aussi pour ne pas oublier de l'upload
from picoTFT_UI import *

from micropython import alloc_emergency_exception_buf
alloc_emergency_exception_buf(100) # permet de voir si jamais des exceptions dans les handlers

def grid_clicked(bt:Button):
    print(f"{bt.name} clicked")

def new_buttons(r,c,r_h=30,c_w=18):
    for r_i in range(r):
        for c_i in range(c):
            bt = Button(f"bt{r_i}_{c_i}",Rect(80+c_i*(c_w+2), r_i*(r_h+2),c_w,r_h), grid_clicked, backColor=grey)
            TFTui.add_control(bt)

def reset_ui():
    print("Reset UI")
    TFTui.redraw()

TFTui = picoTFT_UI()
bt_reset = Button("bt_reset",Rect(0,0,70,45), lambda bt: reset_ui(), label="reset")
TFTui.add_controls([bt_reset])
new_buttons(10,20)
reset_ui()

try:
    while True:
        TFTui.manage_ctrls_callback()
    
except KeyboardInterrupt:
    pass

TFTui.cleanup()
print("- bye -")