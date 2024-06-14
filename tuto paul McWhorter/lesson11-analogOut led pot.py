''' Lesson 10 analog output
'''
from machine import Pin, PWM, ADC
from time import sleep
from pgtools import *
outPin=12
analogOut=PWM(Pin(outPin))
analogOut.freq(1000) # 1kHz
analogOut.duty_u16(0)
analogOut2=PWM(Pin(13))
analogOut2.freq(1000) # 1kHz
analogOut2.duty_u16(0)
potPin=28
myPot = ADC(potPin) # analog IN, ADC2

linCv = LinearConverter(272, 65535, 0, 65535)
# on fait varier 1 led entre les valeurs 0 et 65535 de manière linéaire.
# Le truc c'est que notre oeil voit bien la variation au début mais à partir d'un certain point on ne voit plus la led briller plus.
# Pour bien voir la led s'illuminer de + en + sur toutes les valeurs du potentiomètre, on va changer la valeur par puissance de 2.
# Pour cela on va utiliser un autre linear converter pour obtenir une plage de puissance de 2 allant de 0 (2**0=1) à 16 (2**16=65536),
# puis on calculera la luminosité et pour bien distinguer on changera une autre led
#linCv2 = LinearConverter(272, 65535, 0, 16)
# On peut encore aller + loin, au lieu d'avoir 16 étapes, on peut en faire autant qu'on veut et on va calculer la valeur qui doit être
#  mise à la puissance pour obtenir le bon
brightness_steps = 50   # dans le cas précédent on était à 16
linCv2 = LinearConverter(272, 65535, 0, brightness_steps)
val_to_pow = 65535 ** (1/brightness_steps)   # si brightness_steps vaut 16, val_to_pow sera égale à 2

while (True):
    try:
        potVal=myPot.read_u16()
        pwmVal=linCv.conv(potVal)
        expVal=linCv2.conv(potVal)
        brightness=val_to_pow ** round(expVal)   # puissances de 2 : 1, 2, 4, 8, 16, ..., 65536
        print(potVal, pwmVal, brightness)
        analogOut.duty_u16(int(pwmVal))
        analogOut2.duty_u16(int(brightness))
        sleep(.1)
    except KeyboardInterrupt: # Ctrl-C
        break

analogOut.duty_u16(0)
analogOut2.duty_u16(0)
print("\n"+'prog end')
