# IMPORTATION DE MODULES

import random

"""
Module backend du jeu.

Ce module contient l'ensemble de la logique interne du jeu :
- gestion des jetons
- génération de la grille
- vérifications de connexité
- gestion du ratelier
- sauvegarde / restauration des parties

Auteur : Mohamed MECHACHTI ABEKHTI
"""

###############################################################################
# CLASSE JETON SIMPLE
###############################################################################


class Jeton:
    def __init__(self, couleur=int, etat=int):
        """
        Initialise un jeton avec une couleur et un état.

        :param couleur: (int) identifiant numérique de la couleur
        :param etat: (int) 1 si le jeton est visible, 0 s'il est caché
        """
        self.couleur = couleur
        self.etat = etat

    def __repr__(self):
        """
        Retourne une représentation lisible du jeton.
        
        :return: (str) représentation du jeton
        """
        return f"Jeton({self.couleur},{self.etat})"

    def get_couleur(self):
        """
        Retourne la couleur du jeton.

        :return: (int) identifiant de la couleur
        """
        return self.couleur

    def get_etat(self):
        """
        Retourne l'état du jeton.

        :return: (int) 1 si visible, 0 si caché
        """
        return self.etat

    def verif_jouable(self):
        """
        Vérifie si le jeton est jouable (face visible).

        :return: (bool) True si jouable, False sinon
        """
        if self.get_etat() == 1:
            return True
        elif self.get_etat() == 0:
            return False

    def change_etat(self):
        """
        Change l'état du jeton (visible ↔ caché).
        """
        if self.etat == 0:
            self.etat = 1
        else:
            self.etat = 0

###############################################################################
# CLASSE JETON SPECIAUX (BONUS/MALUS)
###############################################################################

class JetonSpecial:
    def __init__(self, couleur=int, etat=int, fonction=str):
        """
        Initialise un jeton spécial avec une couleur, un état et une fonction.

        :param couleur: (int) identifiant numérique de la couleur
        :param etat: (int) 1 si visible, 0 si caché
        :param fonction: (str) caractéristique du jeton :
                         "givepoints" (bonus),
                         "losepoints" (malus),
                         "multicolor" (multicouleur),
                         "fakejeton" (faux jeton)
        """
        self.couleur = couleur
        self.etat = etat
        if fonction not in ("givepoints", "losepoints", "multicolor", "fakejeton"):
            raise ValueError("Erreur : Ce type de jeton n'existe pas")
        self.fonction = fonction

    def __repr__(self):
        """
        Retourne une représentation lisible du jeton spécial.
        
        :return: (str) représentation du jeton spécial
        """
        return f"JetonSpecial({self.couleur},{self.etat},{self.fonction})"

    def get_couleur(self):
        """
        Retourne la couleur du jeton.

        :return: (int) identifiant de la couleur
        """
        return self.couleur

    def get_etat(self):
        """
        Retourne l'état du jeton.

        :return: (int) 1 si visible, 0 si caché
        """
        return self.etat

    def get_fonction(self):
        """
        Retourne la fonction du jeton spécial.

        :return: (str) fonction du jeton
        """
        return self.fonction

    def change_etat(self):
        """
        Change l'état du jeton (visible ↔ caché).
        """
        if self.etat == 0:
            self.etat = 1
        else:
            self.etat = 0

###############################################################################
# CLASSE PILES DE JETONS
###############################################################################

class JetonPile:
    def __init__(self, nb_jeton):
        """
        Initialise une pile de jetons.

        :param nb_jeton: (int) nombre de jetons dans la pile (3, 6 ou 9)
        """
        if nb_jeton not in (3, 6, 9):
            raise ValueError("Erreur : nb_jeton doit être 3, 6 ou 9")
        self.nombre_jeton = nb_jeton
        self.liste = []

    def gen_list(self):
        """
        Génère une liste vide de jetons avec la taille spécifiée.
        """
        for i in range(self.nombre_jeton):
            self.liste.append(0)

    def est_vide(self):
        """
        Vérifie si la pile est vide.

        :return: (bool) True si vide, False sinon
        """
        if len(self.liste) == 0:
            return True
        else:
            return False

    def get_first_elem(self):
        """
        Renvoie l'élément au sommet de la pile.

        :return: (Jeton or 0) jeton du sommet ou 0 si pile vide
        """
        if self.est_vide():
            return 0
        else:
            return self.liste[-1]

    def get_last_elem(self):
        """
        Renvoie l'élément en bas de la pile.

        :return: (Jeton or None) jeton du bas ou None si pile vide
        """
        if self.est_vide():
            return None
        return self.liste[0]

    def change_etat(self):
        """
        Change l'état du jeton au sommet de la pile.
        """
        premier = self.get_first_elem()
        if premier is not None and premier != 0:
            if isinstance(premier, Jeton):
                premier.change_etat()

    def retirer_jeton(self):
        """
        Retire le jeton du sommet de la pile.

        :return: (Jeton or None) jeton retiré ou None si pile vide
        """
        if not self.est_vide():
            jeton_sup = self.liste.pop()
            self.nombre_jeton = len(self.liste)

            if not self.est_vide():
                premier = self.liste[-1]
                if premier != 0 and isinstance(premier, Jeton) and premier.etat == 0:
                    premier.change_etat()
            return jeton_sup
        return None

    def get_etat(self):
        """
        Retourne l'état du jeton au sommet de la pile.

        :return: (int) état du jeton (1 visible, 0 caché)
        """
        if not self.est_vide():
            return self.get_first_elem().get_etat()

    def __repr__(self):
        """
        Retourne une représentation lisible de la pile.
        
        :return: (str) représentation de la pile
        """
        return f"JetonPile({self.nombre_jeton},{self.liste})"

###############################################################################
# PARAMÈTRES DE JEU
###############################################################################

def difficultes(dif=int):
    """
    Retourne le nombre de couleurs et de cases noires selon la difficulté.

    :param dif: (int) 0=facile, 1=normal, 2=difficile
    :return: (tuple) (nb_couleur, nb_cases_noires)
    """
    if dif == 0:  # facile
        nb_couleur = 5
        nb_cases_noires = 14
    elif dif == 1:  # normal
        nb_couleur = 7
        nb_cases_noires = 23
    elif dif == 2:  # difficile
        nb_couleur = 8
        nb_cases_noires = 26
    elif dif == 3:
        nb_couleur = 6
        nb_cases_noires = 35
    else:
        raise ValueError("Erreur : Difficulté doit être 0, 1, 2 ou 3")
    return nb_couleur, nb_cases_noires


def nb_triplets(dif=int, piles=False, special=False):
    """
    Retourne le nombre de triplets par couleur selon la difficulté et les options.

    :param dif: (int) difficulté (0=facile, 1=normal, 2=difficile)
    :param piles: (bool) True si les piles sont activées
    :param special: (bool) True si les jetons spéciaux sont activés
    :return: (list or tuple) liste des triplets ou (nb_piles, liste_triplets)
    """
    if dif not in (0, 1, 2):
        raise ValueError("Erreur : Difficulté doit être 0, 1 ou 2")
    
    if piles == False:
        if special == False:
            if dif == 0:  # facile
                return [5, 5, 4, 4, 4]
            elif dif == 1:  # normal
                return [3, 3, 3, 3, 3, 2, 2]
            elif dif == 2:  # difficile
                return [3, 2, 2, 2, 3, 2, 2, 2]
        else:
            if dif == 0:  # facile
                return [5, 5, 4, 4, 3]
            elif dif == 1:  # normal
                return [3, 3, 3, 3, 3, 2, 1]
            elif dif == 2:  # difficile
                return [3, 2, 2, 2, 3, 2, 2, 1]

    elif piles == True:
        if special == False:
            if dif == 0:  # facile
                nb_piles = 12
                return (nb_piles, [9, 6, 7, 8, 8])
            elif dif == 1:  # normal
                nb_piles = 9
                return (nb_piles, [2, 3, 2, 5, 6, 7, 5])
            elif dif == 2:  # difficile
                nb_piles = 6
                return (nb_piles, [2, 2, 2, 4, 3, 3, 5, 3])
        else:
            if dif == 0:  # facile
                nb_piles = 12
                return (nb_piles, [9, 6, 7, 8, 7])
            elif dif == 1:  # normal
                nb_piles = 9
                return (nb_piles, [2, 3, 2, 5, 6, 7, 4])
            elif dif == 2:  # difficile
                nb_piles = 6
                return (nb_piles, [2, 2, 2, 4, 3, 3, 5, 2])

###############################################################################
# GRILLE
###############################################################################

class Grille:
    def __init__(self, dif=int, piles=False, special=False):
        """
        Initialise une grille de jeu.

        :param dif: (int) difficulté (0=facile, 1=normal, 2=difficile, 3=extreme)
        :param piles: (bool) True pour activer les piles de jetons
        :param special: (bool) True pour activer les jetons spéciaux
        """
        if dif not in (0, 1, 2, 3):
            raise ValueError("Erreur : Difficulté doit être 0, 1, 2 ou 3")
        
        self.grille = [[0 for x in range(8)] for y in range(10)]
        self.dif = dif
        self.nb_couleurs, self.nb_cases_noires = difficultes(self.dif)
        self.piles = piles
        self.special = special

    def generation_cases_neutres(self):
        """
        Place aléatoirement les cases noires (None) dans la grille.
        """
        for i in range(self.nb_cases_noires):
            a = random.randint(0, 9)
            b = random.randint(0, 7)
            while self.grille[a][b] == None:
                a = random.randint(0, 9)
                b = random.randint(0, 7)
            self.grille[a][b] = None

    def liste_des_jetons_simples(self):
        """
        Génère la liste des jetons simples selon la difficulté.

        :return: (list) liste des jetons
        """
        liste_jetons = []
        if self.piles == False:
            nb_trip = nb_triplets(self.dif, self.piles, self.special)
            for i in range(len(nb_trip)):
                for j in range(nb_trip[i]):
                    for k in range(3):
                        liste_jetons.append(Jeton(i + 1, 1))
            return liste_jetons
        else:
            nb_piles, nb_trip = nb_triplets(self.dif, self.piles, self.special)
            for i in range(len(nb_trip)):
                for j in range(nb_trip[i]):
                    for k in range(3):
                        liste_jetons.append(Jeton(i + 1, 0))
            return liste_jetons

    def placement_des_jetons(self):
        """
        Place les jetons dans la grille.
        """
        if self.piles == False:
            # Génération et mélange des jetons
            liste_jetons = self.liste_des_jetons_simples()
            random.shuffle(liste_jetons)

            index = 0
            # Parcours de la grille
            for i in range(10):
                for j in range(8):
                    # On ne remplace pas les cases noires (None)
                    if self.grille[i][j] is not None:
                        if index < len(liste_jetons):
                            jeton = liste_jetons[index]
                            index += 1
                            # Première ligne : jetons visibles
                            if i == 0:
                                if type(jeton) == Jeton:
                                    if jeton.etat == 0:
                                        jeton.change_etat()
                            else:
                                if type(jeton) == Jeton:
                                    if jeton.etat == 1:
                                        jeton.change_etat()

                            self.grille[i][j] = jeton
                        else:
                            # Sécurité si plus de jetons
                            self.grille[i][j] = 0
        else:
            liste_jetons_simples = self.liste_des_jetons_simples()
            random.shuffle(liste_jetons_simples)
            nb_piles, liste_triplettes = nb_triplets(self.dif, self.piles, self.special)

            # Positions aléatoires pour les piles
            positions_piles = []
            while len(positions_piles) < nb_piles:
                x = random.randint(0, 9)
                y = random.randint(0, 7)
                if self.grille[x][y] is not None:
                    if (x, y) not in positions_piles:
                        positions_piles.append((x, y))

            # Placer chaque pile
            if self.dif == 0:
                tailles_piles = [3, 3, 3, 3, 3, 3, 6, 6, 6, 6, 9, 9]
            elif self.dif == 1:
                tailles_piles = [3, 3, 3, 3, 3, 6, 6, 6, 9]
            elif self.dif == 2:
                tailles_piles = [3, 3, 3, 3, 6, 6]

            random.shuffle(tailles_piles)

            i = 0
            while i < nb_piles:
                x, y = positions_piles[i]
                taille = tailles_piles[i]

                nv_pile = JetonPile(taille)
                nv_pile.gen_list()
                self.grille[x][y] = nv_pile
                i += 1

            # Remplir les piles avec des jetons
            jetons_pour_piles = []

            for coord in positions_piles:
                x, y = coord
                jetonpile = self.grille[x][y]
                for _ in range(jetonpile.nombre_jeton):
                    jetons_pour_piles.append(liste_jetons_simples.pop(0))

            index = 0
            for coord in positions_piles:
                x, y = coord
                jetonpile = self.grille[x][y]
                for i in range(jetonpile.nombre_jeton):
                    jetonpile.liste[i] = jetons_pour_piles[index]
                    index += 1

            # Placer les jetons simples restants
            index = 0
            for x in range(10):
                for y in range(8):
                    if self.grille[x][y] is not None and self.grille[x][y] == 0:
                        if index < len(liste_jetons_simples):
                            self.grille[x][y] = liste_jetons_simples[index]
                            index += 1

            # Rendre visibles les jetons de la première ligne
            for y in range(8):
                case = self.grille[0][y]
                if case is not None and case != 0:
                    if isinstance(case, Jeton):
                        if case.etat == 0:
                            case.change_etat()
                    elif isinstance(case, JetonPile):
                        case.change_etat()

            for x in range(1, 10):
                for y in range(8):
                    case = self.grille[x][y]
                    if isinstance(case, JetonPile):
                        jeton_haut = case.get_first_elem()
                        if isinstance(jeton_haut, Jeton):
                            jeton_haut.etat = 0

    def placement_jetons_speciaux(self):
        """
        Place les jetons spéciaux dans la grille (bonus, malus, faux jetons).
        """
        if self.special == True:
            nb_bonus = 0
            nb_malus = 0
            nb_fake = 0
            # Placement des jetons "givepoints"
            while nb_bonus < 3:
                x = random.randint(0, 9)
                y = random.randint(0, 7)
                if isinstance(self.grille[x][y], Jeton) and not isinstance(self.grille[x][y], JetonSpecial):
                    jeton = self.grille[x][y]
                    etat = jeton.get_etat()
                    couleur = jeton.get_couleur()
                    self.grille[x][y] = JetonSpecial(couleur, etat, "givepoints")
                    nb_bonus += 1

            # Placement des jetons "losepoints"
            while nb_malus < 3:
                x = random.randint(0, 9)
                y = random.randint(0, 7)
                if isinstance(self.grille[x][y], Jeton) and not isinstance(self.grille[x][y], JetonSpecial):
                    jeton = self.grille[x][y]
                    etat = jeton.get_etat()
                    couleur = jeton.get_couleur()
                    self.grille[x][y] = JetonSpecial(couleur, etat, "losepoints")
                    nb_malus += 1

            # Placement des jetons "fakejeton"
            while nb_fake < 3:
                x = random.randint(0, 9)
                y = random.randint(0, 7)
                if self.grille[x][y] == 0:
                    if y == 0:
                        etat = 1
                    else:
                        etat = 0
                    couleur = random.randint(1, self.nb_couleurs)
                    self.grille[x][y] = JetonSpecial(couleur, etat, "fakejeton")
                    nb_fake += 1

        else:
            raise ValueError("Erreur : Vérifiez que l'option special est bien activée")

    def reset_grille(self):
        """
        Réinitialise la grille à un état vide.
        """
        self.grille = [[0 for x in range(8)] for y in range(10)]

    def verif_grille_vide(self):
        """
        Vérifie si la grille est vide.

        :return: (bool) True si vide, False sinon
        """
        if self.grille == [[0 for x in range(8)] for y in range(10)]:
            return True
        else:
            return False

    def est_coin(self, x, y):
        """
        Vérifie si la case est un coin de la grille.

        :param x: (int) coordonnée ligne
        :param y: (int) coordonnée colonne
        :return: (bool) True si coin, False sinon
        """
        if (x == 0 and y == 0) or (x == 0 and y == 7) or (x == 9 and y == 0) or (x == 9 and y == 7):
            return True

    def est_bord(self, x, y):
        """
        Vérifie si la case est sur un bord de la grille.

        :param x: (int) coordonnée ligne
        :param y: (int) coordonnée colonne
        :return: (bool) True si bord, False sinon
        """
        if not self.est_coin(x, y):
            if y == 0 or y == 7 or x == 0 or x == 9:
                return True
            else:
                return False

    def verif_vide(self):
        """
        Vérifie s'il y a des cases vides dans la grille.

        :return: (bool) True si vide trouvé, False sinon
        """
        for x in range(10):
            for y in range(8):
                if self.grille == None or self.grille == 0:
                    return True
                else:
                    return False

    def liste_voisins(self, x, y):
        """
        Retourne la liste des voisins d'une case.

        :param x: (int) coordonnée ligne
        :param y: (int) coordonnée colonne
        :return: (tuple) (liste_voisins, liste_coords) ou None si case vide/neutre
        """
        liste_voisins = []
        liste_coordonnees_voisins = []
        # Si la case est neutre ou vide, elle est "jouable" (ignorable)
        if self.grille[x][y] is None or self.grille[x][y] == 0:
            return None

        if not self.est_coin(x, y) and not self.est_bord(x, y):
            # Case centrale
            liste_voisins.append(self.grille[x - 1][y])
            liste_coordonnees_voisins.append((x - 1, y))

            liste_voisins.append(self.grille[x + 1][y])
            liste_coordonnees_voisins.append((x + 1, y))

            liste_voisins.append(self.grille[x][y - 1])
            liste_coordonnees_voisins.append((x, y - 1))

            liste_voisins.append(self.grille[x][y + 1])
            liste_coordonnees_voisins.append((x, y + 1))

        elif self.est_coin(x, y):
            if x == 0 and y == 0:
                liste_voisins.append(self.grille[x][1])
                liste_coordonnees_voisins.append((x, 1))

                liste_voisins.append(self.grille[1][y])
                liste_coordonnees_voisins.append((1, y))

            elif x == 0 and y == 7:
                liste_voisins.append(self.grille[x][6])
                liste_coordonnees_voisins.append((x, 6))

                liste_voisins.append(self.grille[1][y])
                liste_coordonnees_voisins.append((1, y))

            elif x == 9 and y == 0:
                liste_voisins.append(self.grille[8][y])
                liste_coordonnees_voisins.append((8, y))

                liste_voisins.append(self.grille[x][1])
                liste_coordonnees_voisins.append((x, 1))

            elif x == 9 and y == 7:
                liste_voisins.append(self.grille[8][y])
                liste_coordonnees_voisins.append((8, y))

                liste_voisins.append(self.grille[x][6])
                liste_coordonnees_voisins.append((x, 6))

        elif self.est_bord(x, y):
            if y == 0:
                liste_voisins.append(self.grille[x - 1][y])
                liste_coordonnees_voisins.append((x - 1, y))

                liste_voisins.append(self.grille[x][y + 1])
                liste_coordonnees_voisins.append((x, y + 1))

                liste_voisins.append(self.grille[x + 1][y])
                liste_coordonnees_voisins.append((x + 1, y))

            elif y == 7:
                liste_voisins.append(self.grille[x - 1][y])
                liste_coordonnees_voisins.append((x - 1, y))

                liste_voisins.append(self.grille[x][y - 1])
                liste_coordonnees_voisins.append((x, y - 1))

                liste_voisins.append(self.grille[x + 1][y])
                liste_coordonnees_voisins.append((x + 1, y))

            elif x == 0:
                liste_voisins.append(self.grille[x][y + 1])
                liste_coordonnees_voisins.append((x, y + 1))

                liste_voisins.append(self.grille[x][y - 1])
                liste_coordonnees_voisins.append((x, y - 1))

                liste_voisins.append(self.grille[x + 1][y])
                liste_coordonnees_voisins.append((x + 1, y))

            elif x == 9:
                liste_voisins.append(self.grille[x][y + 1])
                liste_coordonnees_voisins.append((x, y + 1))

                liste_voisins.append(self.grille[x][y - 1])
                liste_coordonnees_voisins.append((x, y - 1))

                liste_voisins.append(self.grille[x - 1][y])
                liste_coordonnees_voisins.append((x - 1, y))

        return liste_voisins, liste_coordonnees_voisins

    def verif_connexion(self, x, y, deja_vus=None):
        """
        Vérifie si le jeton en (x,y) est connecté à la première ligne.

        :param x: (int) abscisse du jeton
        :param y: (int) ordonnée du jeton
        :param deja_vus: (set) ensemble des cases déjà visitées (récursif)
        :return: (bool) True si connecté, False sinon
        """
        # Initialisation de l'ensemble des cases déjà visitées
        if deja_vus is None:
            deja_vus = set()

        # Si déjà sur la première ligne
        if x == 0:
            return True

        # Si case vide ou neutre
        if self.grille[x][y] is None or self.grille[x][y] == 0:
            return False

        # Marquer cette case comme visitée
        deja_vus.add((x, y))

        # Obtenir les voisins
        liste_voisins, liste_coords = self.liste_voisins(x, y)

        # Explorer récursivement chaque voisin valide
        for i in range(len(liste_voisins)):
            voisin = liste_voisins[i]
            coord_voisin = liste_coords[i]

            # Vérifier si le voisin est valide et pas déjà visité
            if (voisin is not None and voisin != 0 and (isinstance(voisin, Jeton) or isinstance(voisin, JetonPile))
                    and coord_voisin not in deja_vus):

                # Appel récursif
                if self.verif_connexion(coord_voisin[0], coord_voisin[1], deja_vus):
                    return True

        return False

    def verifier_grille(self):
        """
        Vérifie que TOUS les jetons de la grille sont connectés à la première ligne.

        :return: (bool) True si tous connectés, False sinon
        """
        for x in range(10):
            for y in range(8):
                # Si c'est un jeton valide
                if (self.grille[x][y] is not None and self.grille[x][y] != 0 and (isinstance(self.grille[x][y], Jeton) or isinstance(self.grille[x][y], JetonPile) or isinstance(self.grille[x][y], JetonSpecial))):
                    # Vérifier sa connexion à la première ligne
                    if not self.verif_connexion(x, y):
                        return False
        return True
    
    def corriger_grille(self):
        if self.special:
            for x in range(1, 9):
                for y in range(8):
                    if (self.grille[x][y] is not None and self.grille[x][y] != 0 and (isinstance(self.grille[x][y], Jeton) or isinstance(self.grille[x][y], JetonPile) or isinstance(self.grille[x][y], JetonSpecial))):
                        if self.grille[x][y].etat==1:
                            self.grille[x][y].change_etat()

    
    def melanger_jetons(self):
        """
        Mélange tous les jetons de la grille sauf :
        - Les cases noires (None)
        - Les jetons de la première ligne
        """
        # 1. Récupérer tous les jetons (Jeton, JetonSpecial, JetonPile) sauf première ligne et cases noires
        jetons_a_melanger = []
        positions = []

        for x in range(1, 10):  # lignes 1 à 9
            for y in range(8):
                case = self.grille[x][y]
                if case is not None:  # on ignore les cases noires
                    jetons_a_melanger.append(case)
                    positions.append((x, y))
                if (isinstance(case, Jeton) or isinstance(case, JetonPile) or isinstance(case, JetonSpecial)):
                    if case.get_etat()==1:
                        case.change_etat()

        # 2. Mélanger la liste des jetons
        random.shuffle(jetons_a_melanger)

        # 3. Remettre les jetons mélangés dans la grille
        for i in range(len(positions)):
            x, y = positions[i]
            self.grille[x][y] = jetons_a_melanger[i]


    def grille_alea(self, profondeur=0):
        """
        Génère une grille aléatoire valide.

        :param profondeur: (int) compteur de récursion (sécurité)
        :return: (list) grille générée
        """
        print(profondeur)
        if profondeur > 10000:
            raise RuntimeError("ERREUR: Impossible de générer une grille valide")
        
        self.reset_grille()
        self.generation_cases_neutres()
        self.placement_des_jetons()
        self.melanger_jetons()

        if self.special == True:
            self.reset_grille()
            self.generation_cases_neutres()
            self.placement_des_jetons()
            self.melanger_jetons()
            self.placement_jetons_speciaux()
            self.corriger_grille()
            
        else:
            self.reset_grille()
            self.generation_cases_neutres()
            self.placement_des_jetons()
            self.melanger_jetons()

        if self.verifier_grille():
            return self.grille
        else:
            return self.grille_alea(profondeur + 1)

###############################################################################
# CLASS RÂTELIER
###############################################################################

class Ratelier:
    def __init__(self, type_jeu=str):
        """
        Initialise un ratelier.

        :param type_jeu: (str) "solo" ou "multi"
        """
        self.type_jeu = type_jeu

        if self.type_jeu in {"solo", "multi"}:
            if self.type_jeu == "solo":
                self.ratelier = [0, 0, 0, 0, 0]
            elif self.type_jeu == "multi":
                self.ratelier = [0, 0, 0, 0, 0]
        else:
            raise ValueError("Erreur de code : Merci de saisir (solo) ou (multi)")

    def verif_plein(self):
        """
        Vérifie si le ratelier est plein.

        :return: (bool) True si plein, False sinon
        """
        for elt in self.ratelier:
            if elt == 0:
                return False
        return True

    def verif_vide(self):
        """
        Vérifie si le ratelier est vide.

        :return: (bool) True si vide, False sinon
        """
        if self.ratelier == [0, 0, 0, 0, 0]:
            return True
        else:
            return False

    def ajouter_elem(self, elem):
        """
        Ajoute un élément dans la première case vide.

        :param elem: élément à ajouter
        """
        assert isinstance(elem, Jeton) or (isinstance(elem, JetonSpecial) and elem.fonction in ("givepoints", "losepoints")) or elem==None, "Erreur : Si vous essayer de rajouter un objet python de type JetonSpecial et de fonction (fakejeton), merci de le convertir en None afin de l'insérer dans le râtelier."
        if not self.verif_plein():
            for i in range(len(self.ratelier)):
                if self.ratelier[i] == 0:
                    self.ratelier[i] = elem
                    break

    def nombre_elements(self):
        """
        Compte le nombre d'éléments dans le ratelier.

        :return: (int) nombre d'éléments
        """
        compteur = 0
        for elt in self.ratelier:
            if elt != 0:
                compteur += 1
        return compteur

    def vider_ratelier(self):
        """
        Vide complètement le ratelier.
        """
        if self.type_jeu == "solo":
            self.ratelier = [0, 0, 0, 0, 0]
        elif self.type_jeu == "multi":
            self.ratelier = [0, 0, 0, 0, 0]

    def effacer_jeton(self, case):
        """
        Efface le jeton à la case spécifiée.

        :param case: (int) index de la case (0 à 4)
        """
        if self.type_jeu == "solo":
            if not (0 <= case <= 4):
                raise ValueError("Erreur : case doit être entre 0 et 4")
            if self.ratelier[case] != 0:
                self.ratelier[case] = 0
        elif self.type_jeu == "multi":
            if not (0 <= case <= 4):
                raise ValueError("Erreur : case doit être entre 0 et 4")
            if self.ratelier[case] != 0:
                self.ratelier[case] = 0
    
    def rajouter_case_neutre(self):
        """
        Méthode dédié à l'ajout d'une case neutre
        """
        if not self.verif_plein():
            self.ajouter_elem(None)
    
    def retirer_case_neutre(self):
        """
        Méthode qui sert à retirer une case neutre du râtelier
        """
        i=0
        if None in self.ratelier:
            effectue=False
            while not effectue:
                if i<5:
                    if self.ratelier[i]==None:
                        self.ratelier[i]=0
                        effectue=True
                    else:
                        i+=1