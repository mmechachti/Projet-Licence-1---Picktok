# 🎮 PickTok

PickTok est un jeu de plateau numérique développé en Python pour l’association **Game Fan-Attic** et réalisé par la startup **Sampple**.  
Il propose une expérience stratégique mêlant réflexion, gestion du râtelier et prise de risque, jouable en **solo** ou en **multijoueur local**.

---

## 🧩 Principe du jeu

Le jeu se déroule sur une grille de **10×8 cases** contenant des jetons colorés (visibles ou cachés), des piles de jetons et des jetons spéciaux (bonus/malus).  
Les joueurs capturent des jetons pour les placer dans un **râtelier commun** afin de former des **triplettes de même couleur** et marquer des points.

La grille est générée aléatoirement à chaque partie, garantissant une forte rejouabilité.

---

## 🕹️ Modes de jeu

### Mode solo
- Gestion individuelle du score
- Objectif : vider la grille
- Bonus de 20 points si la grille est entièrement vidée

### Mode multijoueur
- Râtelier commun
- Tours de jeu alternés
- Le joueur posant le dernier jeton d’une triplette marque les points
- Une erreur peut entraîner la défaite immédiate

---

## ⚙️ Fonctionnalités

- 3 niveaux de difficulté (facile, normal, difficile)
- Génération aléatoire de la grille
- Piles de jetons (3, 6 ou 9)
- Jetons spéciaux :
  - Bonus (+5 points)
  - Malus (-5 points)
  - Faux jeton (case noire temporaire dans le râtelier)
- Sauvegarde automatique (jusqu’à 5 sauvegardes)
- Retour au coup précédent
- Mode daltonien
- Interface graphique avec EiffelTK

---

## 🐞 Bugs connus (pre-release)

- L’annulation d’un coup impliquant un faux jeton peut laisser une case noire permanente dans le râtelier.
- Les informations concernant le tour des joueurs en multijoueur sont encore insuffisantes.

---

## 🗂️ Structure du projet

```
sources/                # Code source Python
icones/                 # Icônes du jeu
saves/                  # Sauvegardes automatiques
fichiers_d_installation/# Installateur Windows
```

---

## ▶️ Lancer le jeu

### Windows
- Python 3.11 requis
- Installer via l’installateur fourni
- Désinstallation via le panneau de configuration

### Linux / macOS
```bash
cd sources
python3 main.py
```

---

## 💾 Sauvegardes

- Sauvegarde automatique à chaque interaction
- Maximum de 5 sauvegardes
- Pour conserver une sauvegarde :
  - copier le dossier `saveX` hors du dossier `saves`
  - le remettre plus tard si besoin (en respectant le nom `save1` à `save5`)

---

## 🛠️ Technologies utilisées

- Langage : Python 3.11
- Interface graphique : EiffelTK
- Sauvegarde : Pickle
- Compatibilité : Windows, Linux, macOS

---

## 👨‍💻 Équipe

Projet développé par **Sampple** :
- Mohamed Mechachti Abekhti – Chef de projet & Backend
- Gabriel Alves Verissimo – Interface graphique & Design
- Faddy El Sisi – Affichage dynamique & règles du jeu

📧 Contact :  
mechachtiabekh@edu.univ-eiffel.fr

---

## 📜 Licence

Projet distribué sous licence **MIT**.
