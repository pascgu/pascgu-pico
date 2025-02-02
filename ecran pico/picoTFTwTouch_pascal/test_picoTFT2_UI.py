from machine import Pin, SPI
from sys import implementation
from os import uname
from utime import sleep
# import ili9341, gt911, gt911_constants as gt #PG: je le laisse ici pour ne pas oublier d'upload ces 3 fichiers .py
from colors import *
# from picoTFTwTouch import * #PG: je le laisse aussi pour ne pas oublier de l'upload
from picoTFT_UI import *

last_points=[]
last_points_while_managing=[]
def on_touch_interrupt(points):
    global in_manage_on_touch
    # PG: ATTENTION dans ce callback, on se trouve dans une interruption donc il est préférable que le code soit
    #     minimal et d'avoir les gros traitements (y compris l'affichage) dans le "while True" principal,
    #     comme c'est fait pour les boutons avec picoTFT_UI.manage_ctrls_callback()
    if points:
        for i in range(len(points)):
            pt = points[i]
            # print(f"  Touch {i+1}: {pt.x}, {pt.y}, size: {pt.size}")
            # TFTui.display.fill_circle(pt.x, pt.y, 2, green)
            if in_manage_on_touch:
                last_points_while_managing.append(pt)
                # if not pt in last_points2:
                #     last_points2.append(pt)
            #elif not pt in last_points:
            else:
                last_points.append(pt)

in_manage_on_touch=False
def manage_on_touch():
    global last_points, last_points_while_managing, in_manage_on_touch
    in_manage_on_touch = True
    points = last_points
    if points:
        #print("Received touch events:")
        for i in range(0,len(points)):
            pt = points[i]
            #print(f"  Touch {i+1}: {pt.x}, {pt.y}, size: {pt.size}")
            #TFTui.display.fill_circle(pt.x, pt.y, 2, green)
            TFTui.display.draw_pixel(pt.x, pt.y, green)
    last_points=last_points_while_managing
    in_manage_on_touch = False
    last_points_while_managing=[]

def reset_ui():
    global bt2_i, bt3_i
    print("Reset UI")
    TFTui.redraw()
    bt2_i=0 ; bt3_i=0

bt2_i=0
def bt2_clicked(bt:Button):
    global bt2_i
    txt = f"Button2 clicked {bt2_i} times"
    print(txt)
    TFTui.draw_text8x8(bt.rect.x+bt.rect.w+10, bt.rect.y+5, txt, cyan)
    bt2_i+=1

bt3_i=0
def bt34_clicked(bt:Button):
    global bt3, bt3_i, bt4
    txt3 = f"Button {bt.label.strip()} clicked {bt3_i} times"
    txt4 = f"Button {bt.label.strip()} clicked"
    if bt==bt3:
        print(txt3)
        TFTui.draw_text8x8(bt.rect.x+bt.rect.w+10, bt.rect.y+5, txt3, cyan)
        TFTui.draw_text8x8(bt4.rect.x+bt4.rect.w+10, bt4.rect.y+5, txt4, black) # efface si un msg bt4 clicked
        bt3_i+=1
        # sleep(1)
        # TFTui.draw_text8x8(bt.rect.x+bt.rect.w+10, bt.rect.y+5, txt3, black)
    else:
        print(txt4)
        TFTui.draw_text8x8(bt.rect.x+bt.rect.w+10, bt.rect.y+5, txt4, cyan)
    # PG: ATTENTION dans tous ces callback, ça reste des interruptions donc il est préférable que le code soit
    #     minimal et d'avoir dans le "while True" principal la gestion des boutons qui ont été cliqués
    # PG: en fait j'ai eu une autre idée, c'est de jouer tous ces callback non pas lors de l'interrupt
    #     qui sera géré en interne par picoTFT_UI mais de les jouer dans la
    #     boucle principale: TFTui.manage_buttons_click().

TFTui = picoTFT_UI(on_touch_interrupt)
bt1 = Button(Rect(0,0,100,45), "refresh", lambda bt: reset_ui())
bt2 = Button(Rect(0,50,100,45), "auto-click", bt2_clicked, autoclick=True)
bt3 = Button(Rect(0,100,100,90), "bt3     ", bt34_clicked)
bt4 = Button(Rect(50,130,50,45), "bt4", bt34_clicked, backColor=white)
TFTui.add_controls([bt1,bt2,bt3,bt4])
reset_ui()

try:
    while True:
        TFTui.manage_ctrls_callback()
        manage_on_touch()
        sleep(0.01)
except KeyboardInterrupt:
    pass

TFTui.cleanup()
print("- bye -")