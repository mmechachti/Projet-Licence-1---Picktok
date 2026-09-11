"""
Auteur : Gabriel Alves Verissimo
Date : Janvier 2026
Description : Module gérant l'affichage graphique du jeu (plateau, jetons, scores)
en utilisant la bibliothèque fltk.
"""

# --- Imports ---

import re
import fltk
import backend

# --- Constantes ---
# Les constantes sont écrites en majuscules

COULEUR_FOND = "#0F172A"
COULEUR_ACCENT = "#2979FF"
COULEUR_BLANC = "white"
COULEUR_NOIR = "black"

# --- Variables Globales ---

liste_jeton = []
liste_ratelier = []


# --- Définitions des fonctions ---


def affichage_grille():
    """
    Dessine la structure statique du plateau de jeu, incluant le fond,
    la grille principale, le râtelier et le logo.
    :return: None
    """
    fltk.efface_tout()
    fltk.rectangle(0, 0, 800, 600, remplissage=COULEUR_FOND)
    
    # Zones de jeu (Grille, Râtelier, etc.)
    fltk.rectangle(20, 50, 420, 550, remplissage=COULEUR_BLANC)
    fltk.rectangle(440, 300, 490, 550, remplissage=COULEUR_BLANC)
    fltk.rectangle(510, 300, 780, 550, remplissage=COULEUR_BLANC)

    # Lignes horizontales de la grille
    for i in range(12):
        fltk.ligne(20, 50 + (i * 50), 420, 50 + (i * 50))
        
    # Lignes verticales de la grille
    for y in range(9):
        fltk.ligne(20 + (y * 50), 50, 20 + (y * 50), 550)

    # Lignes du râtelier
    for i in range(6):
        fltk.ligne(440, 300 + (i * 50), 490, 300 + (i * 50))
    
    for y in range(2):
        fltk.ligne(440 + (y * 50), 300, 440 + (y * 50), 550)

    # Logo et crédits
    fltk.texte(620, 145, "PickTok", taille=40, ancrage="center", couleur=COULEUR_ACCENT)
    fltk.texte(620, 182, "Sampple®", ancrage="center", taille=20, couleur=COULEUR_ACCENT)


def dessin_jeton(x, y, numero, face, couleur, pile):
    """
    Dessine un jeton spécifique ou une pile à une position donnée.
    Ajoute l'objet graphique créé à la liste globale liste_jeton.
    :param x: (int) Coordonnée x de base
    :param y: (int) Coordonnée y de base
    :param numero: (int) Identifiant numérique du jeton/case
    :param face: (int) État du jeton (1: visible, 0: caché, -1: case noire)
    :param couleur: (str) Couleur du jeton
    :param pile: (int) Indicateur si c'est une pile (1) ou non (0)
    :return: None
    """
    if face == 1:
        # Jeton visible
        liste_jeton.append(fltk.cercle(45 + x, 75 + y, 10, tag="cercle" + str(numero), remplissage=couleur, couleur=couleur, epaisseur=23))
    elif face == 0:
        # Jeton caché (contour seulement ou représentation vide)
        liste_jeton.append(fltk.cercle(45 + x, 75 + y, 10, tag="cercle" + str(numero), remplissage=couleur, couleur=couleur, epaisseur=1))
    elif face == -1:
        # Case injouable (noire)
        liste_jeton.append(fltk.rectangle(20 + x, 50 + y, 70 + x, 100 + y, tag="rectangle", remplissage=COULEUR_NOIR))
    elif pile == 1 and face == 1:
        # Pile de jetons
        for i in range(len(backend.JetonPile)): 
            liste_jeton.append(fltk.cercle(45 + x, 75 + y, 10, tag="cercle" + str(numero), remplissage=couleur, couleur=couleur, epaisseur=23))


def creation_jeton(grille_obj=backend.Grille, couleur_aleatoire=list):
    """
    Parcourt l'objet grille du backend et initialise l'affichage de tous les jetons.
    :param grille_obj: (Objet) L'objet grille contenant les données du jeu
    :param couleur_aleatoire: (list) Liste de mapping des couleurs
    :return: None
    """
    a, b = 0, -50
    num = 1

    longueur_grille = grille_obj.grille  

    for i in range(len(longueur_grille)):
        b += 50
        a = 0
        for y in range(len(longueur_grille[i])):
            cellule = longueur_grille[i][y]

            # Cas d'une Pile
            if type(cellule) == backend.JetonPile:
                # Afficher le jeton du dessus de la pile
                jeton_dessus = cellule.get_first_elem()
                couleur = couleur_aleatoire[jeton_dessus.couleur]
                etat = jeton_dessus.etat
                dessin_jeton(a, b, num, etat, couleur, 0)
                
                # Afficher le nombre de jetons dans la pile
                liste_pile_pos = creation_pile("cercle" + str(num), [y, i])
                modifier_pile("cercle" + str(num), liste_pile_pos, str(cellule.nombre_jeton))
            
            # Cas d'un Jeton normal
            elif type(cellule) == backend.Jeton:
                couleur = couleur_aleatoire[cellule.couleur]
                etat = cellule.etat
                dessin_jeton(a, b, num, etat, couleur, 0)
            
            # Cas d'un Jeton spécial
            elif type(cellule) == backend.JetonSpecial:
                couleur = couleur_aleatoire[cellule.couleur]
                etat = cellule.etat
                dessin_jeton(a, b, num, etat, couleur, 0)
            
            # Cases noires (None)
            elif cellule is None:
                dessin_jeton(a, b, num, -1, COULEUR_NOIR, 0)

            a += 50
            num += 1


def deplacement_verification(grille=backend.Grille, abscisse=float, ordonnee=float):  
    """
    Vérifie si un clic aux coordonnées données correspond à une case valide de la grille.
    :param grille: (Objet) L'objet grille du backend
    :param abscisse: (float) Coordonnée X du clic
    :param ordonnee: (float) Coordonnée Y du clic
    :return: (tuple) (tag de la case, [ligne, colonne]) ou (None, None) si invalide
    """
    ligne = ordonnee - 50
    colonne = abscisse - 20
    numero_colonne = colonne // 50
    numero_ligne = ligne // 50
    
    # Conversion en entiers pour les indices
    numero = [int(numero_ligne), int(numero_colonne)]
    longueur_grille = grille.grille
    
    # Vérification des limites et de l'existence de la case
    if longueur_grille[int(numero_ligne)][int(numero_colonne)] is not None:
        numero_case = (int(numero_ligne) * 8) + int(numero_colonne) + 1
        tag_case = "cercle" + str(numero_case)
        return tag_case, numero
    else:
        return None, None


def deplacement(case, place, pos_cercle, couleur_aleatoire, grille_obj=backend.Grille):
    """
    Gère l'affichage du déplacement d'un jeton vers le râtelier.
    :param case: (str) Tag de la case source
    :param place: (int) Position cible dans le râtelier
    :param pos_cercle: (list) Coordonnées [ligne, colonne] dans la grille
    :param couleur_aleatoire: (list) Liste des couleurs
    :param grille_obj: (Objet) L'objet grille du backend
    :return: None
    """
    chiffres = re.search(r'\d+', case)
    numero_case = int(chiffres.group(0))
    longueur_grille = grille_obj.grille
    
    cellule = longueur_grille[pos_cercle[0]][pos_cercle[1]]
    
    if cellule == 0 or cellule is None:
        return
    
    # Récupération de la couleur selon le type de cellule
    if type(cellule) == backend.JetonPile:
        couleur = couleur_aleatoire[cellule.get_first_elem().couleur]
    else:
        couleur = couleur_aleatoire[cellule.couleur]
    
    x, y = 420, 250 + (place * 50)
    
    # Efface l'ancien jeton et le redessine à la nouvelle position
    fltk.efface("cercle" + str(numero_case))
    fltk.efface("texte" + str(numero_case)) 
    dessin_jeton(x, y, numero_case, 1, couleur, 0)


def visibilite(case):              
    """
    Modifie l'apparence d'un jeton pour le rendre 'visible' (plein).
    :param case: (str) Tag du jeton à modifier
    :return: None
    """
    fltk.modifie(case, epaisseur=23)


def effacer_jeton(case):              
    """
    Supprime un jeton de l'affichage.
    :param case: (str) Tag de la case contenant le numéro
    :return: None
    """
    chiffres = re.search(r'\d+', case)
    numero_case = int(chiffres.group(0))
    fltk.efface("cercle" + str(numero_case))


def affichage_texte(texte, taille, couleur):       
    """
    Affiche un message textuel principal.
    :param texte: (str) Le message
    :param taille: (int) Taille de la police
    :param couleur: (str) Couleur du texte
    :return: None
    """
    fltk.efface("Texte1")
    fltk.texte(515, 350, texte, tag="Texte1", taille=taille, couleur=couleur, police="mcfont")


def score1(texte, taille, couleur):           
    """
    Affiche le score du joueur 1.
    :param texte: (str) Le score à afficher
    :param taille: (int) Taille de la police
    :param couleur: (str) Couleur du texte
    :return: None
    """
    fltk.efface("Score")
    fltk.texte(575, 510, texte, tag="Score", taille=taille, couleur=couleur, police="mcfont")


def score2(texte, taille, couleur):                 
    """
    Affiche le score du joueur 2.
    :param texte: (str) Le score à afficher
    :param taille: (int) Taille de la police
    :param couleur: (str) Couleur du texte
    :return: None
    """
    fltk.efface("Score2")
    fltk.texte(690, 510, texte, tag="Score2", taille=taille, couleur=couleur, police="mcfont")


def creation_pile(case, place):                             
    """
    Affiche l'indicateur numérique sur une pile de jetons.
    :param case: (str) Tag de la case associée
    :param place: (list) Coordonnées [colonne, ligne] relatives pour le calcul
    :return: (list) Coordonnées graphiques [x, y] du texte
    """
    liste_pile = [45 + (place[0] * 50), 75 + (place[1] * 50)]        
    chiffres = re.search(r'\d+', case)
    numero_case = chiffres.group(0)
    fltk.texte(45 + (place[0] * 50), 75 + (place[1] * 50), "1", tag="texte" + str(numero_case), ancrage="center", taille=15, couleur=COULEUR_NOIR)
    return liste_pile


def modifier_pile(case, liste_pile, numero):    
    """
    Met à jour le nombre affiché sur une pile.
    :param case: (str) Tag de la case
    :param liste_pile: (list) Coordonnées [x, y] où afficher le texte
    :param numero: (str) Le nouveau nombre à afficher
    :return: None
    """
    chiffres = re.search(r'\d+', case)                  
    numero_case = chiffres.group(0)
    fltk.efface("texte" + str(numero_case))
    fltk.texte(liste_pile[0], liste_pile[1], numero, tag="texte" + str(numero_case), ancrage="center", taille=15, couleur=COULEUR_NOIR)


def affichage_score():
    """
    Affiche le libellé fixe 'Score:'.
    :return: None
    """
    fltk.texte(640, 480, "Score:", taille=30, ancrage="center", police="Helvetica")


def annuler_coup():
    """
    Dessine le bouton permettant d'annuler le dernier coup.
    :return: None
    """
    fltk.rectangle(320, 555, 420, 595, remplissage=COULEUR_NOIR)
    fltk.texte(370, 577, "ANNULER\n    COUP", taille=12, ancrage="center", couleur=COULEUR_ACCENT)


def case_noire(place):
    """
    Dessine une case noire (masque) à une position donnée dans le râtelier.
    :param place: (int) Index de la position dans le râtelier
    :return: None
    """
    x = 420
    y = 250 + (place * 50)
    fltk.rectangle(x + 20, y + 50, x + 70, y + 100, remplissage=COULEUR_NOIR, tag="casenoire")