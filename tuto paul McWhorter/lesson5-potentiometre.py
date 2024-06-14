''' Lesson 5
'''
import machine
from time import sleep
potPin=28 # ADC2 == GP28
myPot = machine.ADC(potPin) # analog IN, 3 pins possibles : ADC0, ADC1, ADC2

x1=250; x2=65535
y1=0; y2=3.3
y_min=min(y1,y2) ; y_max=max(y1,y2)
#y1=100; y2=0 # version demandée à la fin de la vidéo
#Y=aX+b
a=(y2-y1)/(x2-x1) # pente (d'après 2 points)
b=y1-(a*x1) # ordonnée à l'origine (d'après 1 point) => y1=a*x1+b => b=y1-a*x1
while (True):
    try:
        potVal = myPot.read_u16() # read analog value between 0 and 65535
        # Après tests en affichant les valeurs min/max du potentiomètre, on voit : min=~250 max=65535
        #x1=250; x2=65535
        #y1=0; y2=3.3
        # et on doit convertir cette plage 250-65535 en 0V-3.3V
        #  math : on a 2 points d'une ligne que l'on cherche à calculer pour convertir : pt1=(250,0) pt2=(65535,3.3)
        #         pente = (y2-y1)/(x2-x1) = (3.3-0)/(65535-250) = 3.3/65285
        #         equation de la ligne : y-y1=pente*(x-x1) => y-0=(3.3/65285)*(x-250) => y=(3.3/65285)*x-(250*3.3/65285)
        #         Voltage = pente*X-(x1*pente)
        #         Voltage = (3.3/65285)*potVal-(250*3.3/65285)
        #voltage = (3.3/65285)*potVal-(250*3.3/65285)
        #Y=aX+b
        #a=(y2-y1)/(x2-x1)
        #b=-(x1*a)
        voltage = a*potVal+b
        if (voltage < y_min): voltage=y_min
        if (voltage > y_max): voltage=y_max
        print(potVal, voltage)
        sleep(0.5)
    except KeyboardInterrupt: # Ctrl-C
        break

print("\n"+'prog stop')