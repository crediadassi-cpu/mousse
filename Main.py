# main.py
# c est le fichier principal
# il importe toutes les classes et lance le programme

from Classe import Joueur, Equipe
from Match_Tournoi import Tournoi
from Sport import choisir_sport, choisir_niveau


# fonction pour creer les joueurs
def creer_joueurs():
    joueurs = []

    n = 0
    while n < 2:
        try:
            n = int(input("Combien de joueurs : "))
            if n < 2:
                print("il faut au moins 2 joueurs")
        except ValueError:
            print("entrez un nombre")

    # on choisit le sport UNE SEULE FOIS pour tout le tournoi
    # tous les joueurs doivent jouer le meme sport
    print("\nChoisissez le sport du tournoi (tous les joueurs joueront ce sport) :")
    sport_tournoi = choisir_sport()

    for i in range(n):
        print(f"\n--- Joueur {i+1} ---")
        nom = input("  Nom : ")
        prenom = input("  Prenom : ")
        pseudo = input("  Pseudo : ")
        niveau = choisir_niveau()

        # on assigne le meme sport a tous les joueurs
        j = Joueur(nom, prenom, pseudo, sport_tournoi, niveau)
        joueurs.append(j)

        print(f"\n  joueur {i+1} enregistre :")
        print(j)

    return joueurs


# fonction pour creer les equipes
def creer_equipes():
    equipes = []

    n = 0
    while n < 2:
        try:
            n = int(input("Combien d equipes : "))
            if n < 2:
                print("il faut au moins 2 equipes")
        except ValueError:
            print("entrez un nombre")

    sport = choisir_sport()

    for i in range(n):
        print(f"\n--- Equipe {i+1} ---")
        nom_eq = input("  Nom de l equipe : ")

        nb_j = 0
        while nb_j < 1:
            try:
                nb_j = int(input("  Nombre de joueurs : "))
            except ValueError:
                print("  entrez un nombre")

        joueurs = []
        for j in range(nb_j):
            nom_j = input(f"    Joueur {j+1} : ")
            joueurs.append(Joueur(nom_j, "", nom_j, sport, "N/A"))

        eq = Equipe(nom_eq, joueurs, sport)
        equipes.append(eq)
        print(f"  equipe {nom_eq} creee")

    return equipes


# programme principal
print("\n===============================")
print("  GESTIONNAIRE DE TOURNOI")
print("===============================")

nom_tournoi = input("Nom du tournoi : ")
if nom_tournoi == "":
    nom_tournoi = "Championship"

tournoi = Tournoi(nom_tournoi)

print("\n  1 : Joueurs individuels")
print("  2 : Equipes")
choix = input("Votre choix : ")

if choix == "1":
    participants = creer_joueurs()
else:
    participants = creer_equipes()

for p in participants:
    tournoi.ajouter_participant(p)

print("\n  auto   = scores automatiques")
print("  manuel = vous entrez les scores")
mode = input("Mode : ")

if mode != "auto" and mode != "manuel":
    mode = "manuel"

tournoi.lancer_tournoi(mode)