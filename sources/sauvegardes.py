import pickle
import os

"""
Module sauvegarde du jeu.

Ce module contient les fonctions liées aux sauvegardes et la restauration des parties

Auteur : Mohamed MECHACHTI ABEKHTI, EL SISI Faddy
"""
###############################################################################
# GESTION DES SAUVEGARDES (NOUVELLE VERSION)
###############################################################################

dossiers_emplacement_sauvegardes = ["saves/save1", "saves/save2", "saves/save3", "saves/save4", "saves/save5"]
emplacement_to_int = {"saves/save1":1, "saves/save2":2, "saves/save3":3, "saves/save4":4, "saves/save5":5}

def gestion_dossiers(dossiers):
    """
    Vérifie si les dossier de sauvegardes existent dans leurs emplacement 
    :param dossiers: (list) Liste d'emplacement de dossier
    """
    assert isinstance(dossiers, list), "Erreur : dossiers est de type liste"
    assert len(dossiers)==5, "Erreur : Le nombre d'éléments de saves doît être de 5"
    
    for emplacement in dossiers:
        if isinstance(emplacement, str):
            if not os.path.exists(emplacement):
                os.makedirs(emplacement)
        else:
            raise ValueError("Erreur : Vérifier que les éléments de votre liste sont de type (str)")

def verifier_partie_existe(emplacement, dossiers):
    """
    Fonction qui vérifie la présence d'une partie dans une sauvegarde.
    
    :param emplacement: (str) emplacement de la sauvegarde
    :param dossiers: (list) Liste d'emplacement de dossier
    :return: (bool) True si une partie existe à cet emplacement et False sinon
    """
    assert emplacement in dossiers, "Erreur : Merci de vérifier si l'emplacement donné en paramètre est bien dans la liste dossiers également donnée en paramètre."
    
    elements = ["sauvegarde_choix.pkl", "save_annuler.pkl", "save_reprendre.pkl"]
    for fichier in elements:
        if not os.path.exists(emplacement+"/"+fichier):
            return False
    return True

def reinitialiser_sauvegarde(emplacement, dossiers):
    """
    Fonction qui supprimer les éléments de sauvegardes à l'emplacement donné
    
    :param emplacement: (str) emplacement de la sauvegarde
    :param dossiers: (list) Liste d'emplacement de dossier
    """
    assert emplacement in dossiers, "Erreur : Merci de vérifier si l'emplacement donné en paramètre est bien dans la liste dossiers également donnée en paramètre."
    
    elements = ["sauvegarde_choix.pkl", "save_annuler.pkl", "save_reprendre.pkl"]
    if verifier_partie_existe(emplacement, dossiers):
        for fichier in elements:
            os.remove(emplacement+"/"+fichier)
    else:
        raise ValueError("Message : Ce dossier est déjà vide")

def plus_ancienne_sauvegarde(dossiers):
    """
    Fonction qui recherche la sauvegarde la plus ancienne
    :return: (str) emplacement
    """
    assert isinstance(dossiers, list), "Erreur : dossiers est de type liste"
    assert len(dossiers)==5, "Erreur : Le nombre d'éléments de saves doît être de 5"

    #Si il y a pas d'emplacement libre on cherche la plus ancienne pour la remplacer
    dictionnaire_des_temps = {} #On crée un dictionnaire
    for save in dossiers:
        if verifier_partie_existe(save, dossiers):
            fichier = save+"/save_reprendre.pkl"
            dictionnaire_des_temps[save]=os.path.getmtime(fichier) #On met comme clés les emplacement de sauvegarde et comme valeurs leurs date de création.
    emplacement = min(dictionnaire_des_temps, key=dictionnaire_des_temps.get) #on cherche le minimum parmi les valeurs.
    return emplacement 

def trouver_emplacement_libre(dossiers):
    """
    Fonction qui recherche un emplacement libre pour y placer une sauvegarde
    :param dossiers: (list) Liste d'emplacement de dossier
    :return: (str) emplacement
    """
    assert isinstance(dossiers, list), "Erreur : dossiers est de type liste"
    assert len(dossiers)==5, "Erreur : Le nombre d'éléments de saves doît être de 5"

    for save in dossiers:
        if not verifier_partie_existe(save, dossiers):  #On vérifie d'abord si il existe un emplacement libre
            return save
    emplacement_ancien = plus_ancienne_sauvegarde(dossiers)
    return emplacement_ancien


###############################################################################
# CREATION DES FICHIERS PKL DE SAUVEGARDES
###############################################################################

def sauvegarde_annuler(emplacement, grille, ratelier, score, couleur_alea):
    """
    Sauvegarde l'état du jeu pour la fonction annuler.

    :param grille: (list) état de la grille
    :param ratelier: (list) état du ratelier
    :param score: (int) score actuel
    :param couleur_alea: couleur aléatoire
    :param emplacement: (str) emplacement de la sauvegarde
    """
    data = {"grille": grille, "ratelier": ratelier, "score": score, "couleur_alea": couleur_alea}
    with open(emplacement+"/save_annuler.pkl", "wb") as f:
        pickle.dump(data, f)


def restore_annuler(emplacement):
    """
    Restaure l'état sauvegardé pour annuler.

    :return: (tuple) (grille, ratelier, score, couleur_alea)
    :param emplacement: (str) emplacement de la sauvegarde
    """
    with open(emplacement+"/save_annuler.pkl", "rb") as f:
        data = pickle.load(f)
    return (data["grille"], data["ratelier"], data["score"], data["couleur_alea"])


def sauvegarde_reprendre(emplacement, grille, ratelier, score, couleur_alea):
    """
    Sauvegarde l'état du jeu pour reprendre plus tard.

    :param grille: (list) état de la grille
    :param ratelier: (list) état du ratelier
    :param score: (int) score actuel
    :param couleur_alea: couleur aléatoire
    :param emplacement: (str) emplacement de la sauvegarde
    """
    data = {"grille": grille, "ratelier": ratelier, "score": score, "couleur_alea": couleur_alea}
    with open(emplacement+"/save_reprendre.pkl", "wb") as f:
        pickle.dump(data, f)


def restore_reprendre(emplacement):
    """
    Restaure l'état sauvegardé pour reprendre.

    :param emplacement: (str) emplacement de la sauvegarde
    :return: (tuple) (grille, ratelier, score, couleur_alea)
    """
    with open(emplacement+"/save_reprendre.pkl", "rb") as f:
        data = pickle.load(f)
    return (data["grille"], data["ratelier"], data["score"], data["couleur_alea"])


def sauvegarder_choix(emplacement, choix):
    """
    Sauvegarde les choix de jeu.

    :param emplacement: (str) emplacement de la sauvegarde
    :param choix: (dict) dictionnaire des choix
    """
    with open(emplacement+"/sauvegarde_choix.pkl", "wb") as f:
        pickle.dump(choix, f)


def restaurer_choix(emplacement):
    """
    Restaure les choix sauvegardés.

    :param emplacement: (str) emplacement de la sauvegarde
    :return: (dict) dictionnaire des choix
    """
    with open(emplacement+"/sauvegarde_choix.pkl", "rb") as f:
        return pickle.load(f)