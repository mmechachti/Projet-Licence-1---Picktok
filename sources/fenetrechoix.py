"""
Auteur : Gabriel Alves Verissimo
Date : Janvier 2026
Description : Module gérant l'interface graphique des menus, la sélection de la difficulté
et la gestion des sauvegardes pour le jeu PickTok.
"""

# --- Imports ---

import fltk
import sauvegardes
import jeux

# --- Constantes ---
# Les constantes sont écrites en majuscules 
FONT = "#0F172A"
ACCENT = "#2979FF"


# Variables globales
choix_mode = False
choix_difficulte = None
choix_sauvegarde = None
choix_dalto = False
choix_piles = False
choix_special = False

# --- Définitions des fonctions ---


def affichage_menu():
    """
    Affiche le menu principal du jeu avec les options Solo, Multi, Saves et Rules.
    :return: None
    """
    fltk.efface_tout()
    fltk.rectangle(0, 0, 800, 600, remplissage=FONT)
    fltk.texte(35, 170, "PickTok", taille=80, couleur=ACCENT)
    fltk.texte(45, 270, "by Sampple®", taille=20, couleur=ACCENT)

    # Boutons SAVES et RULES
    fltk.rectangle(35, 530, 210, 585, epaisseur=5, couleur=ACCENT)
    fltk.rectangle(240, 530, 415, 585, epaisseur=5, couleur=ACCENT)
    fltk.texte(120, 562, "SAVES", couleur=ACCENT, taille=25, ancrage="center")
    fltk.texte(330, 562, "RULES", taille=25, couleur=ACCENT, ancrage="center")

    # Menu principal (Solo / Multi)
    fltk.rectangle(530, 165, 730, 220, epaisseur=0)
    fltk.rectangle(530, 325, 740, 380, epaisseur=0)
    fltk.texte(630, 200, "> SOLO", ancrage="center", taille=40, couleur=ACCENT)
    fltk.texte(637, 360, "> MULTI", ancrage="center", taille=40, couleur=ACCENT)


def affichage_difficulte():
    """
    Affiche le menu de sélection de la difficulté et les options de jeu.
    :return: None
    """
    fltk.efface_tout()
    fltk.rectangle(0, 0, 800, 600, remplissage=FONT)
    fltk.texte(30, 170, "PickTok", taille=80, couleur=ACCENT)
    fltk.texte(40, 270, "by Sampple®", taille=20, couleur=ACCENT)

    # Options (Piles, Bonus, Daltonien)
    fltk.rectangle(75, 510, 125, 560, epaisseur=5, couleur=ACCENT)
    fltk.rectangle(200, 510, 250, 560, epaisseur=5, couleur=ACCENT)
    fltk.rectangle(325, 510, 375, 560, epaisseur=5, couleur=ACCENT)
    fltk.texte(100, 585, "Piles", ancrage="center", couleur=ACCENT, taille=15)
    fltk.texte(225, 585, "Bonus/Malus", ancrage="center", couleur=ACCENT, taille=15)
    fltk.texte(350, 585, "Daltonien", ancrage="center", couleur=ACCENT, taille=15)
    
    # Menu des difficultés
    fltk.rectangle(490, 105, 730, 170, epaisseur=0)
    fltk.rectangle(490, 265, 765, 330, epaisseur=0)
    fltk.rectangle(490, 425, 780, 490, epaisseur=0)
    fltk.texte(610, 145, "> Facile", ancrage="center", taille=50, couleur=ACCENT)
    fltk.texte(628, 305, "> Normal", ancrage="center", taille=50, couleur=ACCENT)
    fltk.texte(628, 465, "> Difficile", ancrage="center", taille=50, couleur=ACCENT)

    # Bouton Retour
    fltk.rectangle(10, 10, 100, 45, couleur=ACCENT, epaisseur=3)
    fltk.texte(53, 29, "< RETOUR", couleur=ACCENT, ancrage="center", taille=10)


def affichage_sauvegarde():
    """
    Affiche l'interface de gestion des sauvegardes (chargement et réinitialisation).
    :return: None
    """
    fltk.efface_tout()
    fltk.rectangle(0, 0, 800, 600, remplissage=FONT)
    fltk.texte(30, 170, "PickTok", taille=70, couleur=ACCENT)
    fltk.texte(40, 270, "by Sampple®", taille=20, couleur=ACCENT)

    fltk.texte(594, 150, "SAUVEGARDES", taille=30, couleur=ACCENT, ancrage="center")
    
    # Liste des slots de sauvegarde
    # Espaces autour des opérateurs 
    fltk.texte(550, 250, "> Sauvegarde n°1", taille=20, ancrage="center", couleur=ACCENT)
    fltk.texte(550, 300, "> Sauvegarde n°2", taille=20, ancrage="center", couleur=ACCENT)
    fltk.texte(550, 350, "> Sauvegarde n°3", taille=20, ancrage="center", couleur=ACCENT)
    fltk.texte(550, 400, "> Sauvegarde n°4", taille=20, ancrage="center", couleur=ACCENT)
    fltk.texte(550, 450, "> Sauvegarde n°5", taille=20, ancrage="center", couleur=ACCENT)
    
    # Cases à cocher pour sélection
    for y in range(233, 458, 50):
        fltk.rectangle(675, y, 700, y + 25, couleur=ACCENT, epaisseur=3)

    # Bouton Lancer
    fltk.rectangle(645, 520, 755, 580, couleur=ACCENT, epaisseur=5)
    fltk.texte(700, 555, "Lancer", ancrage="center", couleur=ACCENT, taille=20)

    # Bouton Retour
    fltk.rectangle(10, 10, 100, 45, couleur=ACCENT, epaisseur=3)
    fltk.texte(53, 29, "< RETOUR", couleur=ACCENT, ancrage="center", taille=10)

    # Boutons Reset
    for y in range(233, 458, 50):
        fltk.rectangle(725, y, 775, y + 25, couleur="red", epaisseur=3)
        fltk.texte(749, y + 14, 'Reset', taille=10, ancrage="center", couleur="red")


def modifier_texte(texte):
    """
    Met à jour la zone de texte de notification dans le menu de sauvegarde.
    :param texte: (str) Le message à afficher
    :return: None
    """
    fltk.efface("texte_sauvegarde")
    fltk.texte(20, 500, texte, taille=20, couleur=ACCENT, tag="texte_sauvegarde")


def affichage_regle():
    """
    Affiche les règles du jeu.
    :return: None
    """
    fltk.efface_tout()
    fltk.rectangle(0, 0, 800, 600, remplissage=FONT)

    fltk.texte(400, 40, "REGLES DU JEU", ancrage="center", taille=25, couleur=ACCENT)
    fltk.texte(400, 100, "Vous jouerez sur une grille de 8 par 10 cases avec certaine cases injouables.", taille=15, couleur=ACCENT, ancrage="center")
    fltk.texte(400, 150, "Sur cette grille, des jetons seront présents visibles ou cachés.", taille=15, couleur=ACCENT, ancrage="center")
    fltk.texte(400, 200, "Un râtelier contiendra les jetons choisies jusqu'à 5 au total.", taille=15, couleur=ACCENT, ancrage="center")
    fltk.texte(400, 250, "Votre score augmentera de 1 par triplette de couleur ou de 2\nsi votre triplette remplit le râtelier.", taille=15, couleur=ACCENT, ancrage="center")
    fltk.texte(400, 310, "Votre but est de vider la grille tout en marquant le plus de\npoint possible, finir la grille octroyera un bonus de 10 points.", taille=15, couleur=ACCENT, ancrage="center")
    fltk.texte(400, 370, "Certains jetons seront des bonus ou des malus, vous le découvrirez.\nCes jetons ne seront pas différent des autres.", taille=15, couleur=ACCENT, ancrage="center")
    fltk.texte(400, 570, "Cliquez n'importe où pour revenir en arrière...", taille=15, couleur=ACCENT, ancrage="center")


def menu():
    """
    Gère la boucle événementielle du menu principal.
    Permet la navigation vers les sous-menus (difficulté, règles, sauvegardes).
    :return: None
    """
    global choix_mode, choix_difficulte, choix_sauvegarde
    
    fltk.efface_tout()
    affichage_menu()
    
    while True:
        if choix_mode == "Quitter":
            break
        
        if choix_sauvegarde is not None:
            break
        
        if choix_difficulte is not None:
            break
        
        ev = fltk.attend_ev()
        tev = fltk.type_ev(ev)
        
        if tev == "ClicGauche":
            abs_ev = fltk.abscisse(ev)
            ord_ev = fltk.ordonnee(ev)
            
            # Bouton SAVES
            if 35 < abs_ev < 210 and 530 < ord_ev < 585:
                sauvegarde()
            
            # Bouton RULES
            elif 240 < abs_ev < 415 and 530 < ord_ev < 585:
                affichage_regle()
                fltk.attend_clic_gauche()
                affichage_menu()

            # Bouton SOLO
            elif 530 < abs_ev < 730 and 165 < ord_ev < 220:
                choix_mode = "Solo"
                difficulte()
                
            # Bouton MULTI
            elif 530 < abs_ev < 740 and 325 < ord_ev < 380:
                choix_mode = "Multi"
                difficulte()
                
        elif tev == 'Quitte': 
            break


def difficulte():
    """
    Gère la boucle événementielle du menu de difficulté.
    Permet de configurer les options de jeu (Piles, Bonus, Daltonien).
    :return: None
    """
    global choix_difficulte, choix_piles, choix_special, choix_dalto, choix_mode
    
    fltk.efface_tout()
    affichage_difficulte()
    
    while True:
        ev = fltk.attend_ev()
        tev = fltk.type_ev(ev)
        
        if tev == "ClicGauche":
            abs_ev = fltk.abscisse(ev)
            ord_ev = fltk.ordonnee(ev)
            
            # Option Piles
            if 75 < abs_ev < 125 and 510 < ord_ev < 560:
                if choix_piles is True:
                    fltk.efface("trait1")
                    choix_piles = False
                elif choix_piles is False:
                    fltk.ligne(75, 510, 125, 560, epaisseur=5, couleur=ACCENT, tag="trait1")
                    fltk.ligne(75, 560, 125, 510, epaisseur=5, couleur=ACCENT, tag="trait1")
                    choix_piles = True
            
            # Option Bonus/Special
            elif 200 < abs_ev < 250 and 510 < ord_ev < 560:
                if choix_special is True:
                    fltk.efface("trait2")
                    choix_special = False
                elif choix_special is False:
                    fltk.ligne(200, 510, 250, 560, epaisseur=5, couleur=ACCENT, tag="trait2")
                    fltk.ligne(200, 560, 250, 510, epaisseur=5, couleur=ACCENT, tag="trait2")
                    choix_special = True
            
            # Option Daltonien
            elif 325 < abs_ev < 375 and 510 < ord_ev < 560:
                if choix_dalto is True:
                    fltk.efface("trait3")
                    choix_dalto = False
                elif choix_dalto is False:
                    fltk.ligne(325, 510, 375, 560, epaisseur=5, couleur=ACCENT, tag="trait3")
                    fltk.ligne(325, 560, 375, 510, epaisseur=5, couleur=ACCENT, tag="trait3")
                    choix_dalto = True
            
            # Sélection Difficulté
            elif 490 < abs_ev < 730 and 105 < ord_ev < 170:
                choix_difficulte = 0
                break
            elif 490 < abs_ev < 765 and 265 < ord_ev < 330:
                choix_difficulte = 1
                break
            elif 490 < abs_ev < 780 and 425 < ord_ev < 490:
                choix_difficulte = 2
                break
            
            # Retour
            elif 10 < abs_ev < 100 and 10 < ord_ev < 45:
                fltk.efface_tout()
                affichage_menu()
                choix_dalto = False
                choix_special = False
                choix_piles = False
                break
            
        elif tev == 'Quitte':
            choix_mode = "Quitter"
            break


def sauvegarde():
    """
    Gère la boucle événementielle du menu de sauvegarde.
    Permet de sélectionner, charger ou effacer une sauvegarde.
    :return: None
    """
    global choix_mode, choix_sauvegarde
    
    fltk.efface_tout()
    affichage_sauvegarde()
    
    while True:
        ev = fltk.attend_ev()
        tev = fltk.type_ev(ev)
        
        if tev == "ClicGauche":
            abs_ev = fltk.abscisse(ev)
            ord_ev = fltk.ordonnee(ev)
            
            # Gestion des clics sur les 5 emplacements de sauvegarde
            
            if 675 < abs_ev < 700:
                if 233 < ord_ev < 258:
                    if choix_sauvegarde == 1:
                        choix_sauvegarde = None
                        fltk.efface("trait4")
                    else:
                        fltk.efface("trait4")
                        fltk.ligne(675, 233, 700, 258, epaisseur=3, couleur=ACCENT, tag="trait4")
                        fltk.ligne(675, 258, 700, 233, epaisseur=3, couleur=ACCENT, tag="trait4")
                        choix_sauvegarde = 1
                        
                elif 283 < ord_ev < 308:
                    if choix_sauvegarde == 2:
                        fltk.efface("trait4")
                        choix_sauvegarde = None
                    else:
                        fltk.efface("trait4")
                        fltk.ligne(675, 283, 700, 308, epaisseur=3, couleur=ACCENT, tag="trait4")
                        fltk.ligne(675, 308, 700, 283, epaisseur=3, couleur=ACCENT, tag="trait4")
                        choix_sauvegarde = 2
                        
                elif 333 < ord_ev < 358:
                    if choix_sauvegarde == 3:
                        fltk.efface("trait4")
                        choix_sauvegarde = None
                    else:
                        fltk.efface("trait4")
                        fltk.ligne(675, 333, 700, 358, epaisseur=3, couleur=ACCENT, tag="trait4")
                        fltk.ligne(675, 358, 700, 333, epaisseur=3, couleur=ACCENT, tag="trait4")
                        choix_sauvegarde = 3

                elif 383 < ord_ev < 408:
                    if choix_sauvegarde == 4:
                        fltk.efface("trait4")
                        choix_sauvegarde = None
                    else:
                        fltk.efface("trait4")
                        fltk.ligne(675, 383, 700, 408, epaisseur=3, couleur=ACCENT, tag="trait4")
                        fltk.ligne(675, 408, 700, 383, epaisseur=3, couleur=ACCENT, tag="trait4")
                        choix_sauvegarde = 4
                        
                elif 433 < ord_ev < 458:
                    if choix_sauvegarde == 5:
                        fltk.efface("trait4")
                        choix_sauvegarde = None
                    else:
                        fltk.efface("trait4")
                        fltk.ligne(675, 433, 700, 458, epaisseur=5, couleur=ACCENT, tag="trait4")
                        fltk.ligne(675, 458, 700, 433, epaisseur=3, couleur=ACCENT, tag="trait4")
                        choix_sauvegarde = 5

            # Bouton Lancer
            elif 645 < abs_ev < 755 and 520 < ord_ev < 580:
                if sauvegardes.verifier_partie_existe(jeux.emplacement_choix_sauvegarde(choix_sauvegarde), sauvegardes.dossiers_emplacement_sauvegardes):
                    choix_mode = "restart"
                    break
                else:
                    modifier_texte("Info : Aucune sauvegarde !")
            
            # Bouton Retour
            elif 10 < abs_ev < 100 and 10 < ord_ev < 45:
                fltk.efface_tout()
                affichage_menu()
                choix_sauvegarde = None
                break
            
            # Gestion des boutons Reset
            elif 725<abs_ev<775 and 233<ord_ev<258:
                
                if sauvegardes.verifier_partie_existe(sauvegardes.dossiers_emplacement_sauvegardes[0], sauvegardes.dossiers_emplacement_sauvegardes):
                    sauvegardes.reinitialiser_sauvegarde(sauvegardes.dossiers_emplacement_sauvegardes[0], sauvegardes.dossiers_emplacement_sauvegardes)
                    modifier_texte("Info : Sauvegarde 1 Reinitialisée")
                else:
                    modifier_texte("Info : Emplacement déjà vide")
                
            elif 725<abs_ev<775 and 283<ord_ev<308:
            
               
                if sauvegardes.verifier_partie_existe(sauvegardes.dossiers_emplacement_sauvegardes[1], sauvegardes.dossiers_emplacement_sauvegardes):
                        sauvegardes.reinitialiser_sauvegarde(sauvegardes.dossiers_emplacement_sauvegardes[1], sauvegardes.dossiers_emplacement_sauvegardes)
                        modifier_texte("Info : Sauvegarde 2 Reinitialisée")
                else:
                    modifier_texte("Info : Emplacement déjà vide")
            
            elif 725<abs_ev<775 and 333<ord_ev<358:

                if sauvegardes.verifier_partie_existe(sauvegardes.dossiers_emplacement_sauvegardes[2], sauvegardes.dossiers_emplacement_sauvegardes):
                    sauvegardes.reinitialiser_sauvegarde(sauvegardes.dossiers_emplacement_sauvegardes[2], sauvegardes.dossiers_emplacement_sauvegardes)
                    modifier_texte("Info : Sauvegarde 3 Reinitialisée")
                else:
                    modifier_texte("Info : Emplacement déjà vide")
            
            elif 725<abs_ev<775 and 383<ord_ev<408:
            
                if sauvegardes.verifier_partie_existe(sauvegardes.dossiers_emplacement_sauvegardes[3], sauvegardes.dossiers_emplacement_sauvegardes):
                    sauvegardes.reinitialiser_sauvegarde(sauvegardes.dossiers_emplacement_sauvegardes[3], sauvegardes.dossiers_emplacement_sauvegardes)
                    modifier_texte("Info : Sauvegarde 4 Reinitialisée")
                else:
                    modifier_texte("Info : Emplacement déjà vide")

            elif 725<abs_ev<775 and 433<ord_ev<458:
            
                if sauvegardes.verifier_partie_existe(sauvegardes.dossiers_emplacement_sauvegardes[4], sauvegardes.dossiers_emplacement_sauvegardes):
                    sauvegardes.reinitialiser_sauvegarde(sauvegardes.dossiers_emplacement_sauvegardes[4], sauvegardes.dossiers_emplacement_sauvegardes)
                    modifier_texte("Info : Sauvegarde 5 Reinitialisée")
                else:
                    modifier_texte("Info : Emplacement déjà vide")      
        elif tev == 'Quitte':
            choix_mode = "Quitter"
            break
