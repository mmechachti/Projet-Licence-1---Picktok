import fltk
import fenetrechoix
import jeux
import frontend
import sauvegardes
import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

LARGEUR_FENETRE = 800
HAUTEUR_FENETRE = 600
fltk.cree_fenetre(LARGEUR_FENETRE, HAUTEUR_FENETRE)
fltk.titre_et_icone("PickTok by Sampple®", "icones/icone.ico")
fenetrechoix.menu()

"""
Fichier principal du jeu.

Ce fichier contient les instructions suivantes:
    - Vérification de la présence des fichiers de sauvegarde
    - Gestion des choix de l'utilisateur
    - Lancement de la fonction jeu en fonction des choix de l'utilisateur

Auteurs : EL SISI Faddy, ALVES VERISSIMO Gabriel, MECHACHTI ABEKHTI Mohamed
"""

# Vérification des dossiers
sauvegardes.gestion_dossiers(sauvegardes.dossiers_emplacement_sauvegardes)

# Choix des couleurs selon le mode daltonien
if fenetrechoix.choix_dalto == True:
    couleurs = jeux.COULEURS_DALTONIEN
else:
    couleurs = jeux.COULEURS

# Gestion du mode restart
if fenetrechoix.choix_mode == "restart":
    emplacement = jeux.emplacement_choix_sauvegarde(fenetrechoix.choix_sauvegarde)
    choix = sauvegardes.restaurer_choix(emplacement)
    frontend.affichage_grille()
    frontend.annuler_coup()
    grille, ratelier, score, couleur_alea = sauvegardes.restore_reprendre(emplacement)
    choix_difficulte = grille.dif
    
    piles = grille.piles 
    special = grille.special 
    
    if choix == "Solo":
        mode = "solo"
    else:
        mode = "multi"
    jeux.jeu(mode, choix_difficulte, couleurs, piles, special, restore=True)

# Lancement du jeu selon le mode choisi
if fenetrechoix.choix_mode == "Solo":
    frontend.affichage_grille()
    frontend.annuler_coup()
    jeux.jeu("solo", fenetrechoix.choix_difficulte, couleurs, fenetrechoix.choix_piles, fenetrechoix.choix_special)

elif fenetrechoix.choix_mode == "Multi":
    frontend.affichage_grille()
    frontend.annuler_coup()
    jeux.jeu("multi", fenetrechoix.choix_difficulte, couleurs, fenetrechoix.choix_piles, fenetrechoix.choix_special)

fltk.ferme_fenetre()