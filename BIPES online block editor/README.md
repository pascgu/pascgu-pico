# BIPES project

Aller sur https://bipes.net.br/ide/ 
et choisir "Raspberry Pi Pico" ou "Raspberry Pi Pico W".

Avec cet url on a à disposition un éditeur pour faire du code avec des blocs plutot qu'avec Thonny.

Passer en **français** en cliquant sur l'utilisateur en haut à droite puis tout en bas cliquer sur "english" pour changer la langue.

## install - connexion port série via USB
Le plus compliqué c'est de faire fonctionner la connexion au port série.

Il y a 2 types de connexions : Serial et Network, il faut bien choisir Serial.

Pour vérifier que ça fonctionne, utiliser l'onglet Console. Ca doit afficher ">>>" quand bien connecté.

Parfois j'ai dû déconnecter/reconnecter le pico de l'usb et refaire jusqu'à ce que les ">>>" s'affichent mais après ça fonctionne bien.

Note : attention, il ne faut pas avoir de Thonny déjà connecté au pico.

### Sous Microsoft Edge

Je n'ai eu aucun soucis pour accéder directement, rien à faire.

### Sous firefox

- Installer l'extension : WebSerial for Firefox
- Quand on essaye de se connecter, une popup affiche qu'il faut cliquer sur download pour récupérer un fichier exe à installer. Perso le bouton download ne faisait rien. J'ai du faire clic droit->copier le lien et l'ouvrir dans un autre onglet de firefox. Une fois téléchargé, on peut le lancer (ça gueule que c'est dangereux mais normal).
- il faut peut-être relancer firefox

### Sous chrome

Avant de pouvoir accéder au port série via USB :
- Allez d'abord dans l'URL : chrome://flags
- rechercher "web platform" et activer celle qui se nomme "Experimental Web Platform features"
- Perso, même après ça, je n'ai pas réussi à le faire fonctionner mais j'ai un chrome un peu spécial, normalement ça devrait marcher.


## Tips

### save/load
Pour enregistrer son travail puis le recharger, il faut cliquer sur les icones en haut à droite :
- save blocks to file
- load blocks from file

Cela propose d'enregistrer sous forme de XML mais le nom est forcé (pas top) "workspace.bipes.xml" donc au fur et à mesure qu'on enregistre, on a des "workspace.bipes(2).xml", "workspace.bipes(3).xml"...

On a la même possibilité depuis l'icone utilisateur et Projet, il y a une icone pour enregistrer le projet.

### partager

On peut partager assez facilement grace à une icone en haut à droite, la plus proche du bouton "start/stop".

Ca met un peu de temps quand on clique dessus (on a l'impression qu'il ne se passe rien), mais au bout de 10 secondes, ça génère une url unique qu'on peut partager, ex: https://bipes.net.br/ide/?lang=fr#e3to9s

### onglet Files
Permet de voir les fichiers générés par l'outil.

Permet aussi de voir les fichiers sur le pico.

### led intégrée
Attention la led intégrée ne fonctionne pas avec le Pico W parce qu'il force Pin(25) au lieu de Pin('LED').<br>
Pour contourner ceci, utiliser une variable : myLed et la définir à un texte "LED" puis utiliser cette variable dans "set output pin"