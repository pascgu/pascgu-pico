''' Lesson 6
'''

while (True):
    try:
        # input() attend que l'utilisateur saisisse quelque chose (== readline)
        myInput=float(input('Input your number: '))
        if myInput==5:
            print('your number is 5!')
        if myInput<5:
            print('your number is <5!')
        if myInput>5:
            print('your number is >5!')
    except KeyboardInterrupt: # Ctrl-C
        break

print("\n"+'prog stop')