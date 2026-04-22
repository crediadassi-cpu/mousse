# match_tournoi.py
# ce fichier contient les classes Match et Tournoi
# Match gere un match entre 2 participants
# Tournoi gere tout le tournoi

import random


# classe Match
class Match:

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.score1 = None
        self.score2 = None
        self.vainqueur = None

    # methode pour jouer le match
    def jouer(self, mode="manuel"):
        print(f"\n  Match : {self.p1} vs {self.p2}")

        if mode == "auto":
            self.score1 = random.randint(0, 10)
            self.score2 = random.randint(0, 10)
            # on evite egalite
            while self.score1 == self.score2:
                self.score2 = random.randint(0, 10)
        else:
            # mode manuel : on entre les scores
            ok = False
            while ok == False:
                try:
                    self.score1 = int(input(f"  Score de {self.p1} : "))
                    self.score2 = int(input(f"  Score de {self.p2} : "))
                    if self.score1 == self.score2:
                        print("  egalite pas permise, recommencez")
                    else:
                        ok = True
                except ValueError:
                    print("  entrez un nombre entier")

        # on determine le vainqueur
        if self.score1 > self.score2:
            self.vainqueur = self.p1
        else:
            self.vainqueur = self.p2

    # methode pour afficher le resultat
    def afficher(self):
        print(f"  {self.p1} [{self.score1}] - [{self.score2}] {self.p2}  =>  gagnant : {self.vainqueur}")


# classe Tournoi
class Tournoi:

    def __init__(self, nom):
        self.nom = nom
        self.participants = []
        self.tour = 1

    # ajouter un participant au tournoi
    def ajouter_participant(self, p):
        self.participants.append(p)

    # afficher tous les participants
    def afficher_participants(self):
        print("\n==== LISTE DES PARTICIPANTS ====")
        i = 1
        for p in self.participants:
            print(f"\n  Joueur numero {i} :")
            print(p)
            i = i + 1
        print("================================")

    # creer les matchs du tour
    def generer_matchs(self):
        random.shuffle(self.participants)
        matchs = []
        qualifie = None

        # si nombre impair un joueur passe directement
        if len(self.participants) % 2 != 0:
            qualifie = self.participants.pop()
            print(f"\n  {qualifie} passe ce tour sans jouer")

        i = 0
        while i < len(self.participants):
            m = Match(self.participants[i], self.participants[i+1])
            matchs.append(m)
            i = i + 2

        return matchs, qualifie

    # jouer un tour complet
    def jouer_tour(self, mode="manuel"):
        print(f"\n===== TOUR {self.tour} =====")
        matchs, qualifie = self.generer_matchs()

        gagnants = []
        for match in matchs:
            match.jouer(mode)
            match.afficher()
            gagnants.append(match.vainqueur)

        if qualifie != None:
            gagnants.append(qualifie)

        self.participants = gagnants
        self.tour = self.tour + 1

    # lancer tout le tournoi
    def lancer_tournoi(self, mode="manuel"):
        print(f"\n===== TOURNOI : {self.nom} =====")
        self.afficher_participants()

        while len(self.participants) > 1:
            self.jouer_tour(mode)

        print(f"\n===== VAINQUEUR FINAL : {self.participants[0]} =====")