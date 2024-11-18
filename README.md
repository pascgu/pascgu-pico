# pascgu-pico
C'est le projet pour les codes tests du pico

## Syntaxe Markdown de ces fichiers README.md
https://www.markdownguide.org/basic-syntax/

## Installer Anaconda
Si erreur "conda not found" :
set PATH=%PATH%;C:\Anaconda3;C:\Anaconda3\Scripts\

https://stackoverflow.com/questions/64149680/how-can-i-activate-a-conda-environment-from-powershell

Si problème \WindowsPowerShell\profile.ps1 cannot be loaded because running scripts is disabled on this system. For more information, see about_Execution_Policies at https:/go.microsoft.com/fwlink/?LinkID=135170.      At line:1 char:3
Dans VSCode : lancer la commande : "Terminal: Select Default Profile" et choisir "Command Prompt" au lieu de Powershell !

## Installer les stubs de micropython pour VScode
https://micropython-stubs.readthedocs.io/en/main/22_vscode.html

pip install -U micropython-rp2-pico_w-stubs --target typings --no-user