# picoTFTwTouch.py

Voilà ma version avec une classe pour gérer à la fois l'affichage et le Touch en 1 seule classe : picoTFTwTouch.py

Pour tester : test_picoTFT1_wTouch.py

# picoTFT_UI.py

Ajout d'une autre classe picoTFT_UI.py qui ajoute la gestion de boutons pour créer des UI.

L'ordre des boutons peut avoir une importance si des boutons sont les uns sur les autres ou dans les autres.

Dans ce cas, si TFTui.addButtons([bt1,bt2]), alors en cas de clic sur une zone commune, c'est bt2 qui aura le clic et bt1 ne sera pas testé. Le z-offset va donc du plus loin au plus proche et c'est le plus proche (celui qui est visible) qui gagne le clic.