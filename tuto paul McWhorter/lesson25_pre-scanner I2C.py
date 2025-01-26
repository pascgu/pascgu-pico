''' Lesson 25 prequisite :
    Si erreur [Errno 5] EIO, File "ssd1306.py", line 115, in write_cmd :
        - installer le scanner pour trouver les périph i2c : https://randomnerdtutorials.com/raspberry-pi-pico-i2c-scanner-micropython/
        - changer les Pin ci-dessous suivant celles utilisées pour SLC et SDA
'''

# I2C Scanner MicroPython
from machine import Pin, SoftI2C

# You can choose any other combination of I2C pins
#i2c = SoftI2C(sda=Pin(26), scl=Pin(27)) # channel 1
#i2c = SoftI2C(sda=Pin(2), scl=Pin(3)) # channel 1
#i2c = SoftI2C(sda=Pin(6), scl=Pin(7)) # channel 1
#i2c = SoftI2C(sda=Pin(0), scl=Pin(1)) # channel 0
i2c = SoftI2C(sda=Pin(20), scl=Pin(21)) # channel 0

print('I2C SCANNER')
devices = i2c.scan()

if len(devices) == 0:
  print("No i2c device !")
else:
  print('i2c devices found:', len(devices))

  for device in devices:
    print("I2C hexadecimal address: ", hex(device))
