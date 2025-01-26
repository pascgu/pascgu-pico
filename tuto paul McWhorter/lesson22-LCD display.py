''' Lesson 22 : Using an LCD Display with the pico W
'''

from lcd1602 import LCD

# Les PIN sont hardcodés dans la lib lcd1602 de cette façon :
#        sda = machine.Pin(6)
#        scl = machine.Pin(7)
# Les 2 autres PIN de l'écran LCD doivent être sur GND et VCC=5V (ex:VBUS)
lcd=LCD() # SDA=Pin(6), SCL=Pin(7), VCC=5V

while True:
    try:
        myName=input('What is your Name ? ')
        if (myName=='q'): break
        greeting1='Hello '+myName
        greeting2='Welcome to My Pi'
        
        lcd.clear()
        column_index = 0
        row_index = 0
        lcd.write(column_index, row_index, greeting1)
        lcd.write(0, 1, greeting2)
        # Si on fait un write avec moins de caractères que la fois précédente, ça n'efface pas la fin (ex ici si on saisi un Name plus court)
        # Pour résoudre ça, il faut soit mettre des espaces à la fin (pas d'erreur si plus de caractères que le LCD)
        #                           soit ajouter lcd.clear() comme j'ai mis là

    except KeyboardInterrupt: # Ctrl-C
        break

print('prog end')
