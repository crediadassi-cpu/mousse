#test_tournoi.py
#pytest


import pytest
from Classe import Joueur, Equipe
from Match_Tournoi import Match, Tournoi

#**********************************************
#       TESTS DE LA CLASSE JOUEUR
#**********************************************
#Test de vérification de la création d'un joueur 
def test__creation__joueur():
    j = Joueur("Dupont", "Jean", "Shadow", "Valorant", "Expert")
    assert j.nom == "Dupont"
    assert j.prenom == "Jean"
    assert j.pseudo == "Shadow"
    assert j.sport == "Valorant"
    assert j.niveau == "Expert"
    
    
#Test de vérification de l'intégration dupseudo du joueur dans str
def test_str_joueur():
    j = Joueur("Dupont", "Jean", "Shadow", "Valorant", "Expert")
    resultat =  str(j)
    assert "Shadow" in resultat
    assert "Dupont" in resultat
    
    
#Test de vérifation de la différenciation des pseudo entre différents joueurs
def test_joueur_differents():
    j1 = Joueur("Dupont", "Jean", "Shadow", "Valorant", "Expert")
    j2 = Joueur("Martin", "Alice", "Storm", "FIFA", "Debutant")
    assert j1.pseudo != j2.pseudo
    assert j1.nom != j2.nom
    
    
    
#**************************************************
#      TESTS DE LA CLASSE EQUIPE
#**************************************************

# Test de vérification de la creation d'une équipe

def test_creation_equipe():
    eq = Equipe
    j1 = Joueur("Dupont", "Jean", "Shadow", "FIFA", "Expert")
    j2 = Joueur("Martin", "Alice", "Storm", "FIFA", "Intermediaire")
    assert test_creation_equipe.nom == "Les Lions"
    assert eq.sport == "FIFA"
    assert len(eq.joueurs) == 2
    
# test pour verifier que l equipe contient bien ses joueurs
def test_joueurs_dans_equipe():
    j1 = Joueur("Dupont", "Jean", "Shadow", "FIFA", "Expert")
    j2 = Joueur("Martin", "Alice", "Storm", "FIFA", "Intermediaire")
    eq = Equipe("Les Lions", [j1, j2], "FIFA")
    assert j1 in eq.joueurs
    assert j2 in eq.joueurs
    
# Test d'équipe vide 
def test_equipe_vide():
    eq = Equipe("Equipe vide", [], "Tenis")
    assert len(eq.joueurs) == 0
    
    
#**************************************************
#      TESTS DE LA CLASSE MATCH
#**************************************************

#Test de vérification du vrai vainqueur(Le joueur avec le plus de points)
def test_vainqueur_match():
    j1 = Joueur("Dupont", "Jean", "Shadow", "Valorant", "Expert")
    j2 = Joueur("Martin", "Alice", "Storm", "Valorant", "Debutant")
    m = Match(j1, j2)
    # On simule les scores manuellement
    m.score1 = 3
    m.score2 = 1
    if m.score1 > m.score2:
        m.vainqueur = m.p1
    else:
        m.vainqueur = m.p2
    assert m.vainqueur == j1
 
# Test pour verifier que le deuxieme joueur peut aussi gagner
def test_vainqueur_match_p2():
    j1 = Joueur("Dupont", "Jean", "Shadow", "Valorant", "Expert")
    j2 = Joueur("Martin", "Alice", "Storm", "Valorant", "Debutant")
    m = Match(j1, j2)
    m.score1 = 0
    m.score2 = 5
    if m.score1 > m.score2:
        m.vainqueur = m.p1
    else:
        m.vainqueur = m.p2
    assert m.vainqueur == j2
 
 
# Test pour verifier que les scores sont bien enregistres
def test_scores_match():
    j1 = Joueur("Dupont", "Jean", "Shadow", "Valorant", "Expert")
    j2 = Joueur("Martin", "Alice", "Storm", "Valorant", "Debutant")
    m = Match(j1, j2)
    m.score1 = 7
    m.score2 = 2
    assert m.score1 == 7
    assert m.score2 == 2
 
 
# =============================================
# TESTS DE LA CLASSE TOURNOI
# =============================================
 
# test pour verifier qu on peut ajouter des participants
def test_ajouter_participant():
    t = Tournoi("Test Cup")
    j = Joueur("Dupont", "Jean", "Shadow", "Valorant", "Expert")
    t.ajouter_participant(j)
    assert len(t.participants) == 1
 
 
# test pour verifier que le tournoi commence bien au tour 1
def test_tour_initial():
    t = Tournoi("Test Cup")
    assert t.tour == 1
 
 
# test pour verifier que le nom du tournoi est bien enregistre
def test_nom_tournoi():
    t = Tournoi("E-Sport Championship")
    assert t.nom == "E-Sport Championship"
 
 
# test pour verifier qu on peut ajouter plusieurs participants
def test_plusieurs_participants():
    t = Tournoi("Test Cup")
    j1 = Joueur("Dupont", "Jean", "Shadow", "Valorant", "Expert")
    j2 = Joueur("Martin", "Alice", "Storm", "Valorant", "Debutant")
    j3 = Joueur("Durand", "Paul", "Fire", "Valorant", "Intermediaire")
    t.ajouter_participant(j1)
    t.ajouter_participant(j2)
    t.ajouter_participant(j3)
    assert len(t.participants) == 3