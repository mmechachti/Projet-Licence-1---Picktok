# ============================================================================
# IMPORTS
# ============================================================================

from backend import *
from frontend import *
import fltk
import random
import sauvegardes
import fenetrechoix

# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

def emplacement_choix_sauvegarde(choix_sauvegarde):
    """
    Fonction qui donne l'emplacement des fichiers de sauvegardes de la restoration choisie par l'utilisateur
    
    :param choix_sauvegarde: (int) Un choix de sauvegarde
    :return: (str) emplacement de la sauvegarde
    """
    assert choix_sauvegarde >= 1 or choix_sauvegarde <= 5, "Erreur : Numéro de sauvegarde indisponible"
    correspondance = {1: "saves/save1", 2: "saves/save2", 3: "saves/save3", 4: "saves/save4", 5: "saves/save5"}
    return correspondance[choix_sauvegarde]

def couleur_aleatoire(couleurs, grille_obj):
    """
    Génère une liste de couleurs aléatoires pour le jeu.
    
    :param couleurs: (list) Liste des couleurs disponibles
    :param grille_obj: (Grille) Objet grille contenant le nombre de couleurs
    :return: (list) Liste de couleurs aléatoires
    """
    couleur_aleatoire = ["rien"]
    couleur_aleatoire2 = random.sample(couleurs, grille_obj.nb_couleurs)
    couleur_aleatoire.extend(couleur_aleatoire2)
    return couleur_aleatoire

def compter_jetons_par_couleur(ratelier):
    """
    Compte le nombre de jetons par couleur dans le ratelier.
    
    :param ratelier: (Ratelier) Objet ratelier contenant les jetons
    :return: (dict) Dictionnaire {couleur: nombre}
    """
    compteur = {}
    for jeton in ratelier.ratelier:
        if jeton != 0 and jeton is not None:
            couleur = jeton.get_couleur()
            compteur[couleur] = compteur.get(couleur, 0) + 1
    return compteur

def trouver_triplet(ratelier):
    """
    Recherche si trois jetons de même couleur sont présents dans le ratelier.
    
    :param ratelier: (Ratelier) Objet ratelier contenant les jetons
    :return: (int or None) Couleur du triplet trouvé ou None si aucun
    """
    compteur = compter_jetons_par_couleur(ratelier)
    for couleur, nombre in compteur.items():
        if nombre >= 3:
            return couleur
    return None

def retirer_triplet_visuel(ratelier, couleur_triplet):
    """
    Retire visuellement trois jetons de même couleur du ratelier.
    
    :param ratelier: (Ratelier) Objet ratelier
    :param couleur_triplet: (int) Couleur du triplet à retirer
    """
    jetons_retires = 0
    for i in range(5):
        if jetons_retires >= 3:
            break
        if ratelier.ratelier[i] != 0 and ratelier.ratelier[i] is not None:
            if ratelier.ratelier[i].get_couleur() == couleur_triplet:
                ratelier.effacer_jeton(i)
                jetons_retires += 1

def redessiner_ratelier(ratelier, Listeratelier, couleur_alea):
    """
    Redessine complètement le ratelier à l'écran.
    
    :param ratelier: (Ratelier) Objet ratelier
    :param Listeratelier: (list) Liste des identifiants graphiques du ratelier
    :param couleur_alea: (list) Liste des couleurs
    """
    # Effacer tous les éléments visuels du ratelier
    for cercle_id in Listeratelier:
        effacer_jeton(cercle_id)
    
    fltk.efface("casenoire")
    Listeratelier.clear()

    position = 0
    for i in range(5):
        if ratelier.ratelier[i] is None:
            case_noire(position)
            position += 1
        elif ratelier.ratelier[i] != 0:
            jeton = ratelier.ratelier[i]
            couleur = couleur_alea[jeton.get_couleur()]
            x = 420
            y = 250 + position * 50
            numero = 100 + position
            dessin_jeton(x, y, numero, 1, couleur, 0)
            Listeratelier.append("cercle" + str(numero))
            position += 1

def calculer_points(ratelier_etait_plein):
    """
    Calcule les points gagnés pour un triplet.
    
    :param ratelier_etait_plein: (bool) True si le ratelier était plein
    :return: (int) Nombre de points (1 ou 2)
    """
    if ratelier_etait_plein:
        return 2
    else:
        return 1

def est_game_over(ratelier):
    """
    Vérifie si la partie est terminée (game over).
    
    :param ratelier: (Ratelier) Objet ratelier
    :return: (bool) True si game over, False sinon
    """
    if ratelier.verif_plein():
        return trouver_triplet(ratelier) is None
    return False

def est_victoire(grille_obj):
    """
    Vérifie si le joueur a gagné (grille vide).
    
    :param grille_obj: (Grille) Objet grille
    :return: (bool) True si victoire, False sinon
    """
    for ligne in grille_obj.grille:
        for case in ligne:
            if case != 0 and case is not None:
                return False
    return True

COULEURS = ["red", "blue", "green", "yellow", "orange", "purple", "pink", "brown", "grey", "cyan", "magenta", "turquoise", "indigo"]
COULEURS_DALTONIEN = ["#0072B2","#56B4E9","#00BFC4","#6A3D9A","#F0E442","#E6C29F","#017374","#4D4D4D","dark green"]

def gerer_voisins(grille, x, y):
    """
    Gère la révélation des voisins d'une case après retrait d'un jeton.
    
    :param grille: (Grille) Objet grille
    :param x: (int) Coordonnée X de la case
    :param y: (int) Coordonnée Y de la case
    """
    resultat = grille.liste_voisins(x, y)
    
    if resultat is None:
        return
    
    liste_voisins, liste_coords_voisins = resultat
    
    for i in range(len(liste_voisins)):
        voisin = liste_voisins[i]
        coord_voisin = liste_coords_voisins[i]
        
        if voisin is not None and voisin != 0:
            numero_case = coord_voisin[0] * 8 + coord_voisin[1] + 1
            
            # Jeton normal ou spécial caché
            if (type(voisin) == Jeton or type(voisin) == JetonSpecial) and voisin.get_etat() == 0:
                voisin.change_etat()
                fltk.modifie("cercle" + str(numero_case), epaisseur=23)
            # JetonPile avec jeton du dessus caché
            elif type(voisin) == JetonPile and voisin.get_first_elem().get_etat() == 0:
                voisin.change_etat()
                fltk.modifie("cercle" + str(numero_case), epaisseur=23)

def gerer_fin_coup(emplacement, ratelier, grille, score_j1, score_j2, mode, joueur_actuel, couleur_alea, Listeratelier, fake_jetons_compteur):
    """
    Gère toutes les actions à la fin d'un coup : scores, triplets, game over, victoire.
    
    :param emplacement: (str) Emplacement de sauvegarde
    :param ratelier: (Ratelier) Objet ratelier
    :param grille: (Grille) Objet grille
    :param score_j1: (int) Score du joueur 1
    :param score_j2: (int) Score du joueur 2
    :param mode: (str) Mode de jeu ("solo" ou "multi")
    :param joueur_actuel: (int) Joueur actuel (1 ou 2)
    :param couleur_alea: (list) Liste des couleurs
    :param Listeratelier: (list) Liste des identifiants graphiques du ratelier
    :param fake_jetons_compteur: (dict) Compteur des fake jetons
    :return: (tuple) Scores mis à jour, joueur actuel, état de la partie
    """
    partie_terminee = False
    
    # Décrémenter les compteurs des fake jetons
    positions_a_supprimer = []
    for pos, tours_restants in list(fake_jetons_compteur.items()):
        fake_jetons_compteur[pos] = tours_restants - 1
        
        if fake_jetons_compteur[pos] == 0:
            if mode == "solo":
                affichage_texte("Retrait de la case noire !", 17, "purple")
            else:
                affichage_texte(f"J{joueur_actuel}: Retrait de la case noire !", 16, "purple")
        
        if fake_jetons_compteur[pos] <= 0:
            positions_a_supprimer.append(pos)
    
    # Supprimer les fake jetons expirés
    for pos in positions_a_supprimer:
        ratelier.retirer_case_neutre()
        del fake_jetons_compteur[pos]
    
    # Redessiner si des fake jetons ont été supprimés
    if positions_a_supprimer:
        redessiner_ratelier(ratelier, Listeratelier, couleur_alea)
    
    # Vérifier si un triplet est formé
    couleur_triplet = trouver_triplet(ratelier)
    
    if couleur_triplet is not None:
        ratelier_etait_plein = ratelier.verif_plein()
        points = calculer_points(ratelier_etait_plein)
        
        if mode == "solo":
            score_j1 += points
        else:
            if joueur_actuel == 1:
                score_j1 += points
            else:
                score_j2 += points
        
        retirer_triplet_visuel(ratelier, couleur_triplet)
        redessiner_ratelier(ratelier, Listeratelier, couleur_alea)
        
        if mode == "solo":
            if points == 2:
                affichage_texte("Triplet ! +2 pts", 25, "green")
            else:
                affichage_texte("Triplet ! +1 pt", 25, "green")
            score1("Score: " + str(score_j1), 25, "black")
        else:
            if points == 2:
                affichage_texte(f"J{joueur_actuel} Triplet ! +2 pts", 25, "green")
            else:
                affichage_texte(f"J{joueur_actuel} Triplet ! +1 pt", 25, "green")
            affichage_score()
            score1(str(score_j1), 25, "black")
            score2(str(score_j2), 25, "black")
    
    # Sauvegarde
    if mode == "solo":
        score_a_sauver = score_j1
    else:
        score_a_sauver = (score_j1, score_j2)
        
    sauvegardes.sauvegarde_reprendre(emplacement, grille, ratelier, score_a_sauver, couleur_alea)
    # Vérifier game over
    if est_game_over(ratelier):
        partie_terminee = True
        if mode == "solo":
            affichage_texte("Perdu !", 20, "red")
            score1("Score final: " + str(score_j1), 20, "red")
        else:
            if joueur_actuel == 1:
                score_j1 = 0
            else:
                score_j2 = 0
            
            affichage_texte(f"J{joueur_actuel} Perdu !\nScore remis à 0", 18, "red")
            affichage_score()
            score1(str(score_j1), 20, "red")
            score2(str(score_j2), 20, "red")
        if sauvegardes.verifier_partie_existe(emplacement, sauvegardes.dossiers_emplacement_sauvegardes):
            sauvegardes.reinitialiser_sauvegarde(emplacement, sauvegardes.dossiers_emplacement_sauvegardes)
    
    # Vérifier victoire
    elif est_victoire(grille):
        partie_terminee = True
        if mode == "solo":
            score_j1 += 10
            affichage_texte("Victoire ! Bonus +10", 20, "gold")
            score1("Score final: " + str(score_j1), 20, "green")
        else:
            if joueur_actuel == 1:
                score_j1 += 10
            else:
                score_j2 += 10
            affichage_texte(f"J{joueur_actuel} Victoire ! Bonus +10", 20, "gold")
            affichage_score()
            score1(str(score_j1), 20, "green")
            score2(str(score_j2), 20, "green")
        if sauvegardes.verifier_partie_existe(emplacement, sauvegardes.dossiers_emplacement_sauvegardes):
            sauvegardes.reinitialiser_sauvegarde(emplacement, sauvegardes.dossiers_emplacement_sauvegardes)
    
    # Changement de joueur en multi (seulement si la partie n'est pas terminée)
    if mode == "multi":
        if joueur_actuel == 1:
            joueur_actuel = 2
        else:
            joueur_actuel = 1
        
    return score_j1, score_j2, joueur_actuel, partie_terminee

def gerer_jeton_special(jeton_retire, mode, joueur_actuel, score_j1, score_j2):
    """
    Gère les bonus/malus des jetons spéciaux et retourne les scores mis à jour.
    
    :param jeton_retire: (JetonSpecial) Jeton spécial retiré
    :param mode: (str) Mode de jeu ("solo" ou "multi")
    :param joueur_actuel: (int) Joueur actuel (1 ou 2)
    :param score_j1: (int) Score du joueur 1
    :param score_j2: (int) Score du joueur 2
    :return: (tuple) Scores mis à jour
    """
    fonction = jeton_retire.get_fonction()
    
    if fonction == "givepoints":
        if mode == "solo":
            score_j1 += 5
            affichage_texte("Bonus ! +5 pts", 22, "gold")
        else:
            if joueur_actuel == 1:
                score_j1 += 5
            else:
                score_j2 += 5
            affichage_texte(f"J{joueur_actuel} Bonus ! +5 pts", 22, "gold")
    
    elif fonction == "losepoints":
        if mode == "solo":
            score_j1 -= 5
            affichage_texte("Malus ! -5 pts", 22, "red")
        else:
            if joueur_actuel == 1:
                score_j1 -= 5
            else:
                score_j2 -= 5
            affichage_texte(f"J{joueur_actuel} Malus ! -5 pts", 22, "red")
    
    # Mise à jour de l'affichage des scores
    if mode == "solo":
        score1("Score: " + str(score_j1), 25, "black")
    else:
        affichage_score()
        score1(str(score_j1), 25, "black")
        score2(str(score_j2), 25, "black")
    
    return score_j1, score_j2

# ============================================================================
# FONCTION PRINCIPALE DE JEU
# ============================================================================

def jeu(mode, dif, couleurs, piles=False, special=False, restore=False):
    """
    Fonction principale qui gère le déroulement d'une partie.
    
    :param mode: (str) Mode de jeu ("solo" ou "multi")
    :param dif: (int) Difficulté (0=facile, 1=normal, 2=difficile, 3=extreme)
    :param couleurs: (list) Liste des couleurs disponibles
    :param piles: (bool) True pour activer les piles
    :param special: (bool) True pour activer les jetons spéciaux
    :param restore: (bool) True pour restaurer une sauvegarde
    """
    peut_annuler = False
    partie_terminee = False
    joueur_coup_precedent = None
    fake_jetons_compteur = {}
    
    # Initialisation selon le mode
    if restore:
        emplacement = emplacement_choix_sauvegarde(fenetrechoix.choix_sauvegarde)
        grille, ratelier, score_saved, couleur_alea = sauvegardes.restore_reprendre(emplacement)
        if mode == "solo":
            score_j1 = score_saved
            score_j2 = 0
        else:
            if isinstance(score_saved, tuple) and len(score_saved) == 2:
                score_j1, score_j2 = score_saved
            else:
                score_j1 = score_saved
                score_j2 = 0
    else:
        emplacement = sauvegardes.trouver_emplacement_libre(sauvegardes.dossiers_emplacement_sauvegardes)
        texte = f"Sauvegarde n°{sauvegardes.emplacement_to_int[emplacement]} initialisée"
        affichage_texte(texte, 15, "red")
        grille = Grille(dif, piles, special)
        grille.grille_alea()
        ratelier = Ratelier(mode)
        score_j1 = 0
        score_j2 = 0
        couleur_alea = couleur_aleatoire(couleurs, grille)
    Listeratelier = []
    creation_jeton(grille, couleur_alea)
    redessiner_ratelier(ratelier, Listeratelier, couleur_alea)
    
    # Affichage du score selon le mode
    if mode == "solo":
        score1("Score: " + str(score_j1), 25, "black")
        joueur_actuel = 1
    else:
        affichage_score()
        score1(str(score_j1), 25, "black")
        score2(str(score_j2), 25, "black")
        joueur_actuel = 1
    
    sauvegardes.sauvegarder_choix(emplacement, "Solo" if mode == "solo" else "Multi")
    
    while True:
        ev = fltk.attend_ev()
        tev = fltk.type_ev(ev)
        if tev == "Quitte":
            break

        if tev == "ClicGauche":
            abs_ev = fltk.abscisse(ev)
            ord_ev = fltk.ordonnee(ev)

            # Bouton ANNULER
            if 320 < abs_ev < 420 and 555 < ord_ev < 595:
                if special:
                    affichage_texte("Annulation désactivée", 18, "red")
                    continue
                if peut_annuler:
                    grille, ratelier, score_saved, couleur_alea = sauvegardes.restore_annuler(emplacement)
                    if mode == "multi":
                        score_j1, score_j2 = score_saved
                        if joueur_coup_precedent is not None:
                            joueur_actuel = joueur_coup_precedent
                    else:
                        score_j1 = score_saved
                    
                    peut_annuler = False
                    partie_terminee = False

                    affichage_grille()
                    annuler_coup()
                    Listeratelier.clear()
                    creation_jeton(grille, couleur_alea)
                    redessiner_ratelier(ratelier, Listeratelier, couleur_alea)
                    
                    if mode == "solo":
                        score1("Score: " + str(score_j1), 25, "black")
                        affichage_texte("Coup annulé !", 18, "orange")
                    else:
                        affichage_score()
                        score1(str(score_j1), 25, "black")
                        score2(str(score_j2), 25, "black")
                        affichage_texte(f"Coup annulé !\nTour de J{joueur_actuel}", 18, "orange")
                else:
                    affichage_texte("Aucun nouveau coup à \nannuler !", 18, "red")

            # Clic sur la grille
            if 20 < abs_ev < 420 and 50 < ord_ev < 550:
                if partie_terminee:
                    continue

                cercle_choisi, Position_cercle = deplacement_verification(grille, abs_ev, ord_ev)
                
                if cercle_choisi is None:
                    affichage_texte("Merci de cliquer sur \nun jeton de face visible", 18, "red")
                    continue

                x, y = Position_cercle
                jeton = grille.grille[x][y]

                # GESTION DES JETONPILES
                if type(jeton) == JetonPile:
                    if jeton.get_first_elem().get_etat() == 0:
                        affichage_texte("Merci de cliquer sur \nune pile de face visible", 18, "red")
                        continue
                    
                    fltk.efface("Texte1")
                    Place = ratelier.nombre_elements()
                    if Place >= 5:
                        continue
                    
                    # Sauvegarde pour annulation
                    if not special:
                        if mode == "multi":
                            joueur_coup_precedent = joueur_actuel
                            sauvegardes.sauvegarde_annuler(emplacement, grille, ratelier, (score_j1, score_j2), couleur_alea)
                        else:
                            sauvegardes.sauvegarde_annuler(emplacement, grille, ratelier, score_j1, couleur_alea)
                    
                    peut_annuler = not special
                    est_dernier_jeton = (jeton.nombre_jeton == 1)
                    
                    jeton_retire = jeton.get_first_elem()
                    numero_case_grille = x * 8 + y + 1
                    fltk.efface("cercle" + str(numero_case_grille))
                    fltk.efface("texte" + str(numero_case_grille))
                    
                    # Vérifier si c'est un jeton spécial
                    if type(jeton_retire) == JetonSpecial:
                        score_j1, score_j2 = gerer_jeton_special(jeton_retire, mode, joueur_actuel, score_j1, score_j2)
                    
                    ratelier.ajouter_elem(jeton_retire)

                    if est_dernier_jeton:
                        gerer_voisins(grille, x, y)
                    
                    jeton.retirer_jeton()
                    redessiner_ratelier(ratelier, Listeratelier, couleur_alea)

                    if jeton.nombre_jeton > 0:
                        nouveau_jeton_dessus = jeton.get_first_elem()
                        couleur_pile = couleur_alea[nouveau_jeton_dessus.get_couleur()]
                        a = y * 50
                        b = x * 50
                        if nouveau_jeton_dessus.get_etat() == 1:
                            etat_visuel = 1
                        else:
                            etat_visuel = 0
                        dessin_jeton(a, b, numero_case_grille, etat_visuel, couleur_pile, 0)
                        ListePile_pos = creation_pile("cercle" + str(numero_case_grille), [y, x])
                        modifier_pile("cercle" + str(numero_case_grille), ListePile_pos, str(jeton.nombre_jeton))
                    else:
                        grille.grille[x][y] = 0
                    
                    score_j1, score_j2, joueur_actuel, partie_terminee = gerer_fin_coup(
                        emplacement, ratelier, grille, score_j1, score_j2, mode, joueur_actuel, couleur_alea, Listeratelier, fake_jetons_compteur
                    )
                
                # GESTION JETONS SPECIAUX
                elif type(jeton) == JetonSpecial:
                    if jeton.get_etat() == 0:
                        affichage_texte("Merci de cliquer sur \nun jeton de face visible", 18, "red")
                        continue
                    
                    Place = ratelier.nombre_elements()
                    if Place >= 5:
                        continue
                    
                    # Sauvegarde pour annulation
                    if not special:
                        if mode == "multi":
                            joueur_coup_precedent = joueur_actuel
                            sauvegardes.sauvegarde_annuler(emplacement, grille, ratelier, (score_j1, score_j2), couleur_alea)
                        else:
                            sauvegardes.sauvegarde_annuler(emplacement, grille, ratelier, score_j1, couleur_alea)
                    
                    peut_annuler = not special
                    fonction = jeton.get_fonction()
                    
                    if fonction == "fakejeton":
                        ratelier.rajouter_case_neutre()
                        fake_jetons_compteur[Place] = 4
                        message = "Fake Jeton !\nCase noire 3 tours"
                        if mode == "multi":
                            message = f"J{joueur_actuel} " + message
                            affichage_texte(message, 18, "purple")
                        else:
                            affichage_texte(message, 20, "purple")
                    else:
                        score_j1, score_j2 = gerer_jeton_special(jeton, mode, joueur_actuel, score_j1, score_j2)
                        ratelier.ajouter_elem(jeton)
                    
                    # Nettoyer la grille
                    numero_case_grille = x * 8 + y + 1
                    fltk.efface("cercle" + str(numero_case_grille))
                    gerer_voisins(grille, x, y)
                    grille.grille[x][y] = 0
                    
                    if fonction != "fakejeton":
                        deplacement(cercle_choisi, Place, Position_cercle, couleur_alea, grille)
                        Listeratelier.append(cercle_choisi)
                    
                    redessiner_ratelier(ratelier, Listeratelier, couleur_alea)
                    score_j1, score_j2, joueur_actuel, partie_terminee = gerer_fin_coup(
                        emplacement, ratelier, grille, score_j1, score_j2, mode, joueur_actuel, couleur_alea, Listeratelier, fake_jetons_compteur
                    )
                
                # GESTION JETONS NORMAUX
                elif type(jeton) == Jeton:
                    if jeton.get_etat() == 0:
                        affichage_texte("Merci de cliquer sur \nun jeton de face visible", 18, "red")
                        continue
                    
                    fltk.efface("Texte1")
                    Place = ratelier.nombre_elements()
                    if Place >= 5:
                        continue
                    
                    # Sauvegarde pour annulation
                    if not special:
                        if mode == "multi":
                            joueur_coup_precedent = joueur_actuel
                            sauvegardes.sauvegarde_annuler(emplacement, grille, ratelier, (score_j1, score_j2), couleur_alea)
                        else:
                            sauvegardes.sauvegarde_annuler(emplacement, grille, ratelier, score_j1, couleur_alea)
                    
                    peut_annuler = not special
                    ratelier.ajouter_elem(jeton)
                    deplacement(cercle_choisi, Place, Position_cercle, couleur_alea, grille)
                    Listeratelier.append(cercle_choisi)
                    gerer_voisins(grille, x, y)
                    grille.grille[x][y] = 0
                    redessiner_ratelier(ratelier, Listeratelier, couleur_alea)
                    
                    score_j1, score_j2, joueur_actuel, partie_terminee = gerer_fin_coup(
                        emplacement, ratelier, grille, score_j1, score_j2, mode, joueur_actuel, couleur_alea, Listeratelier, fake_jetons_compteur
                    )
        
        fltk.mise_a_jour()