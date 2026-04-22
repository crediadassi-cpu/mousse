from Classe import Joueur, Equipe
from Match_Tournoi import Tournoi
from Sport import choisir_sport, choisir_niveau


# Fonstion pour creer les joueurs
def creer_joueurs():
    joueurs = []
    
    n = 0
    while n < 2:
        try:
            n = int(input("Combien de joueurs : "))
            if n< 2 :
                print("il faut au moins 2 joueurs")
        except ValueError:
            print("Entrer un nombre")
            
    print("\nChoisissez le sport du tournoi sur lequel sera evaluer les joueurs: ")
    sport_tournoi = choisir_sport()
    
    for i in range(n):
        print(f"\n-----Joueur {i+1} -----")
        nom = input("  Nom : ")
        prenom = input("  Prenom : ")
        pseudo = input("  Pseudo : ")
        niveau = choisir_niveau()
        
        # Le sport choisie est jouer tout les joueurs
        j = Joueur(nom, prenom, pseudo, sport_tournoi, niveau)
        joueurs.apprend(j)
    
        print(f"\n  joueur {i+1} enregistre : ")
        print(j)
    
        return creer_joueurs


#  Création des équipes
def creer_equipes():
    equipes = []
    
    n = 0
    while n < 2:
        try:
            
            n = int(input("Combien d'équipes : "))
            if n < 2 :
                print("il faut au moins 2 équipes")
        
        except ValueError:
            print("entrez un nombre")
            
            
    sport = choisir_sport()
    
    for i in range(n):
        print(f"\n-----Equipe {i+1}-----")
        nom_eq = input("  Nom de l'équipe : ")
        
        nb_j = 0
        while nb_j < 1:
            try:
                nb_j = int(input("Nombre de joueurs : "))
            except ValueError:
                print("  Entrez un nombre")
                
                
        joueurs = []
        for j in range(nb_j):
            nom_j = input(f"    Joueur {j+1} : ")
            joueurs.append(Joueur(nom_j, "", nom_j, sport, "N/A"))
            
        eq = Equipe(nom_eq, joueurs, sport)
        equipes.append(eq)
        print(f"    Equipe {nom_eq} creee")
        
        
    return equipes



# Programme principale
print("\n****************************")
print("    GESTIONNAIRE DE TOURNOI")
print("\n****************************")


nom_tournoi= input("Nom du tournoi : ")
if nom_tournoi == "":
    nom_tournoi = "Championship"

tournoi = Tournoi(nom_tournoi)

print("\n  1 : Joueurs individuels")
print("  2 : Equipes")
Choix = input("Votre choix : ")

if Choix == "1":
    participants = creer_joueurs()
else:
    participants = creer_equipes()
    
for p in participants:
    tournoi.ajouter_participant(p)
    
print("\n auto  = scores automatiques")
print("  manuel = vous entrez les scores")
mode = input("Mode : ")
if mode != "auto" and mode != "manuel":
    mode = "manuel"
    
tournoi.lancer_tournoi(mode)
    