from utime import sleep, ticks_us, ticks_diff
from ucollections import deque
# import ili9341, gt911, gt911_constants as gt #PG: je le laisse ici pour ne pas oublier d'upload ces 3 fichiers .py
from colors import *
# from picoTFTwTouch import * #PG: je le laisse aussi pour ne pas oublier de l'upload
from picoTFT_drivers import TouchPt
from picoTFT_UI import *

import micropython
micropython.alloc_emergency_exception_buf(100) # permet de voir si jamais des exceptions dans les handlers

points:deque[tuple[int,int,int]]=deque((),100)
def on_touch_interrupted(buff_points, n):
    global points
    # PG: ATTENTION dans ce callback, on se trouve dans une interruption donc il est préférable que le code soit
    #     minimal et d'avoir les gros traitements (y compris l'affichage) dans manage_on_touch() qui est appelé
    #     dans "while True" principal. Il faut éviter l'allocation mémoire, donc deque et tuple c'est le mieux.
    # PG: les buff_points sont des objets qui sont réutilisés à chaque interrupt, il faut donc soit sauver leurs
    #     valeurs, soit les cloner.
    for i in range(n):
        pt:TouchPt=buff_points[i]
        #print(f"{i}: {pt}")
        #TFTui.display.fill_circle(pt.x, pt.y, 2, green)
        points.append((pt.id,pt.x,pt.y))

last_pt = {} # last_pt, one for each ids (chaque doigt correspond à un id différent quand plusieurs touch)
def manage_on_touch():
    global points, last_pt
    if points:
        #print("Received touch events:")
        id,x,y = points.popleft()
        if id==0:
            last_pt_id = last_pt.get(id)
            if last_pt_id is not None:
                last_x,last_y=last_pt_id
                TFTui.display.draw_line(last_x, last_y, x, y, green)
            last_pt[id] = (x,y)
        else:
            TFTui.display.draw_pixel(x, y, green)

def reset_ui():
    global bt2_i, bt3_i, last_pt
    print("Reset UI")
    TFTui.redraw()
    bt2_i=0 ; bt3_i=0
    last_pt = {}

bt2_i=0
def bt2_clicked(bt:Button):
    global bt2_i
    txt = f"Button2 clicked {bt2_i} times"
    print(txt)
    TFTui.draw_text8x8(bt.rect.x+bt.rect.w+10, bt.rect.y+5, txt, cyan)
    bt2_i+=1

bt3_i=0
last_ticks = 0
def bt3_on_interrupt(bt:Button):
    global bt3_i,last_ticks
    bt3_i+=1
    #ticks = ticks_us()
    #print("bt3_on_interrupt",bt3_i,ticks_diff(ticks,last_ticks))
    #last_ticks = ticks
def bt3_clicked_long_process(bt,txt):
    #sleep(1) # ne surtout pas faire ça car cela bloque les interruptions (pas d'interrupt pendant 1s, donc considère nouveau clic)
    TFTui.draw_text8x8(bt.rect.x+bt.rect.w+10, bt.rect.y+5, txt, black)
def bt34_clicked(bt:Button):
    global bt3, bt3_i, bt4, last_ticks
    ticks = ticks_us() ; diff_us=ticks_diff(ticks,last_ticks)
    txt3 = f"Button {bt.label.strip()} clicked {bt3_i} times"
    txt4 = f"Button {bt.label.strip()} clicked"
    last_ticks=ticks
    if bt==bt3:
        #timer.deinit()
        bt.timer().stop()
        print(txt3, diff_us)
        TFTui.draw_text8x8(bt.rect.x+bt.rect.w+10, bt.rect.y+5, txt3, cyan)
        TFTui.draw_text8x8(bt4.rect.x+bt4.rect.w+10, bt4.rect.y+5, txt4, black) # efface si un msg bt4 clicked

        #timer.init(mode=Timer.ONE_SHOT, period=1000, callback=lambda t: bt3_clicked_long_process(bt3,txt3))
        bt.timer().wait(2000, callback=lambda ctrl: bt3_clicked_long_process(ctrl,txt3))
        #bt3_i+=1
        # TODO : quand on active ceci et qu'on clique plusieurs fois sur bt3, ça ne fait rien tant que ceci pas terminé donc on rate des clics. C'est bien ce qu'on veut? Autre type de bouton?
        #sleep(1)
        #TFTui.draw_text8x8(bt.rect.x+bt.rect.w+10, bt.rect.y+5, txt3, black)
    else:
        print(txt4)
        TFTui.draw_text8x8(bt.rect.x+bt.rect.w+10, bt.rect.y+5, txt4, cyan)

TFTui = picoTFT_UI(on_touch_interrupted)
bt1 = Button("bt1",Rect(0,0,100,45), "refresh", lambda bt: reset_ui())
bt2 = Button("bt2",Rect(0,50,100,45), "auto-click", bt2_clicked, autoclick=True)
bt3 = Button("bt3",Rect(0,100,100,90), "bt3     ", bt34_clicked, bt3_on_interrupt)
bt4 = Button("bt4",Rect(50,130,50,45), "bt4", bt34_clicked, backColor=white)
TFTui.add_controls([bt1,bt2,bt3,bt4])
reset_ui()

try:
    while True:
        TFTui.manage_ctrls_callback()
        manage_on_touch()
except KeyboardInterrupt:
    pass

TFTui.cleanup()
print("- bye -")