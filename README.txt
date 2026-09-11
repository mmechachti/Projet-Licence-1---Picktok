#######################################################################
#                                                                     #
#                  Game Fan-attic propose PickTok                     #
#               Développé par Sampple – Janvier 2026                  #
#              Version 1.1 distribuée sous licence MIT                #
#                                                                     #
#######################################################################

# ------------ Notes des développeurs ------------
# - le répertoire 'sources' contient les *.py du programme;
# - le répertoire 'icones' contient les icônes du jeu ;
# - le répertoire 'saves' contient les dossiers de sauvegarde du jeu ;
# - le répertoire 'fichiers_d'installation' contient l'installateur windows du jeu ;
# - backend.py : fonctions liés aux objets Jeton, génération de la grille et gestion du râtelier ;
# - frontend.py : fonctions pour les éléments graphiques du jeu ;
# - fenetrechoix.py : contient les fonctions d'affichage du menu ;
# - jeux.py : contient le moteur du jeu ;
# - sauvegardes.py : contient les fonctions liés aux sauvegardes ;
# - main.py : contient les instructions nécéssaires au lancement du jeu ;
# - LICENCE.txt : contient les informations relatives à la licence de ce jeu ;

# ------------ Notes aux joueurs ------------
# - Si vous êtes sur Windows 7 ou supérieur et que Python3 est installé sur votre machine, vous pouvez directement
    installer nativement le jeu PickTok par Sampple sur votre machine.
    Si vous souhaitez désinstaller le jeu, allez dans le panneau de configuration puis cherchez "PickTok" puis désinstallez le.
# - Si vous êtes sur une distribution linux ou sur MacOS et que Python3 est installé sur votre machine.
    Ouvrez un terminal dans le dossier 'sources' puis tapez la commande 'python3 main.py'.
# - Si vous souhaitez sauvegarder une partie indéfiniment sur votre machine. (ne fonctionne pas pour les utilisateurs ayant installé PickTok nativement sur Windows)
    Rendez vous dans le dossier 'saves' et copier le dossier de sauvegarde qui vous intéresse et collez la en dehors du dossier PickTok.
    Pour la récupérer, copiez là à nouveau depuis le répertoire que vous avez choisi et collez dans le dossier 'saves'.
    Vérifiez bien que le nom du dossier est bien écrit sous la forme 'saveX' où X est un chiffre compris entre 1 et 5.

# ------------ Comment jouer? ------------
# - La première fenêtre comprend 4 boutons :
    - Solo : permet d'afficher le menu de choix de difficulté pour un jeu solitaire
    - Multi : permet d'afficher le menu de choix de difficulté pour un jeu multijoueur
    - Rules : fenêtre qui explique les règles principales du jeu
    - Saves : fenêtre de gestion des sauvegarde. Pour restaurer une sauvegarde particulière, il faut cocher celle qui vous intéresse.
      Pour réinitialiser il suffit de cliquer sur le bouton rouge "reset", un petit message confirme si la réinitialisation a été effectuée.
      ATTENTION : Si vous essayez de restaurer une sauvegarde inexistante, le jeu plantera et c'est tout à fait normal
# - Lorsque vous avez cliqué sur Solo ou Multi vous aurez une fenêtre qui vous invitera à choisir une difficulté (Facile, Normal, Difficile).
    ATTENTION, si vous appuyez directement sur (Facile, Normal, Difficile) le jeu se lancera immédiatement.
    Vous pouvez également choisir des options à cocher (Bonus/Malus, Piles, Daltonien)
# - Dans la fenêtre de jeu vous y trouverez:
    - une grille de 10x8
    - un râtelier de 5 cases 
    - une boite de dialogue vous renvoyant des messages concernant votre partie telles que les
    mises à jour du score, les messages de défaite, avertissements etc...

# ------------ En cas de problèmes ------------
# - Merci de contacter le reférent du groupe Sampple : MECHACHTI ABEKHTI Mohamed
    via l'adresse mail suivante:
    mechachtiabekh@edu.univ-eiffel.fr

    

