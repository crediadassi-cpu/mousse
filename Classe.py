# classes.py
# ici je definie mes classes principales
# Participant est la classe mere
# Joueur et Equipe heritent de Participant

# la classe mere
class Participant:
    def __init__(self, nom):
        self.nom = nom

    def __str__(self):
        return self.nom


# la classe Joueur qui herite de Participant
class Joueur(Participant):

    def __init__(self, nom, prenom, pseudo, sport, niveau):
        super().__init__(nom)
        self.prenom = prenom
        self.pseudo = pseudo
        self.sport = sport
        self.niveau = niveau

    # affichage du joueur dans un cadre pour bien le voir
    def __str__(self):
        sep = "-" * 34
        return (
            f"  +{sep}+\n"
            f"  | Pseudo : {self.pseudo:<24}|\n"
            f"  | Nom    : {self.nom:<24}|\n"
            f"  | Prenom : {self.prenom:<24}|\n"
            f"  | Sport  : {self.sport:<24}|\n"
            f"  | Niveau : {self.niveau:<24}|\n"
            f"  +{sep}+"
        )

    def __repr__(self):
        return f"{self.pseudo} ({self.sport})"


# la classe Equipe qui herite aussi de Participant
class Equipe(Participant):

    def __init__(self, nom, joueurs, sport):
        super().__init__(nom)
        self.joueurs = joueurs
        self.sport = sport

    def __repr__(self):
        return f"{self.nom} ({self.sport}, {len(self.joueurs)} joueurs)"

    # methode pour afficher les joueurs de l equipe
    def afficher_joueurs(self):
        for j in self.joueurs:
            print(" -", j.nom)