#Liste des sports disponibles
SPORTS_DISPONIBLES =[
    "Football",
    "Basketball",
    "Tennis",
    "Volleyball",
    "Handball",
    "Rugby",
    "Baseball",
    "Hockey sur glace",
    "Natation",
    "Athletisme",
    "Cyclisme",
    "Boxe",
    "Judo",
    "Karate",
    "Escrime",
    "Badminton",
    "Ping-pong",
    "Golf",
    "FIFA",
    "League of Legends",
    "Valorant",
    "Counter-Scrike",
    "Fortnite",
    "Rocket Leaugue",
    "Street Fighter",
    "Tekken",
    "Dota 2",
    "Overwatch",
    
]
NIVEAUX_DISPONIBLES = [
    "Débutant",
    "Intermédiaire",
    "Avancé"
    ]


#Afficher la liste des sports
def afficher_sports():
    print("\n===== SPORTS DISPONIBLES =====")
    for i in range(len(SPORTS_DISPONIBLES)):
        print(f"  {i+1}. {SPORTS_DISPONIBLES[i]}")
    print("==============================")
    
    
    
#Demander à l'utilisateur de choisir un sport
def choisir_sport():
    afficher_sports()
    choix = 0
    while choix < 1 or choix > len(SPORTS_DISPONIBLES):
        try:
            choix= int(input("Choisissez un sport (numero) : "))
            if choix < 1 or choix > len(SPORTS_DISPONIBLES):
                print("Numéro invalide, Reessayez")
        except ValueError:
            print("Entrez un nombre")
    return SPORTS_DISPONIBLES[choix - 1]



# afficher la liste des niveaux
def afficher_niveaux():
    print("\n  Niveaux :")
    for i in range(len(NIVEAUX_DISPONIBLES)):
        print(f"    {i+1}. {NIVEAUX_DISPONIBLES[i]}")
 
 
# demander a l utilisateur de choisir un niveau
def choisir_niveau():
    afficher_niveaux()
    choix = 0
    while choix < 1 or choix > len(NIVEAUX_DISPONIBLES):
        try:
            choix = int(input("  Choisissez un niveau (numero) : "))
            if choix < 1 or choix > len(NIVEAUX_DISPONIBLES):
                print("  numero invalide")
        except ValueError:
            print("  entrez un nombre")
    return NIVEAUX_DISPONIBLES[choix - 1]