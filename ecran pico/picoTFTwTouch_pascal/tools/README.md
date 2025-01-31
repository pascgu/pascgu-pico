# scannerI2C.py
Lancer ce fichier sur le pico pour trouver l'adresse utilisé sur l'I2C.

Penser à bien définir les Pin pour l'I2C.


# img2rgb565.py

Pour générer les images RAW utilisables par ili9341, il faut lancer le script img1rgb565.py

- Se mettre dans une commande "activate pico" :

<code>
$ (pico) C:\Users\hotma\source\repos\pascgu-pico\ecran pico\Ecran_TFT_ili9341\test_rdagger>python img2rgb565.py ..\fruit2_480x320.png

Saved: ..\fruit2_480x320.raw
</code>

- exemple d'utilisation des images :

ecran pico\Ecran_TFT_ili9341\test_rdagger\mPico_ili9341_image.py