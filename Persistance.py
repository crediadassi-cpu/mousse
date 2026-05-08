# persistance.py
# ce fichier gere la base de donnees SQLite du projet
# on utilise sqlite3 qui est deja installe avec python
# la base de donnees contient 3 tables : joueurs, equipes, tournois

import sqlite3
import os
from Classe import Joueur, Equipe
from Match_Tournoi import Tournoi

# nom du fichier de la base de donnees
NOM_BASE = "tournoi.db"


# =============================================
# CREATION DE LA BASE DE DONNEES
# =============================================

# cette fonction cree les tables si elles n existent pas encore
def creer_base():
    connexion = sqlite3.connect(NOM_BASE)
    curseur = connexion.cursor()

    # table des tournois
    curseur.execute("""
        CREATE TABLE IF NOT EXISTS tournois (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            tour INTEGER
        )
    """)

    # table des joueurs
    curseur.execute("""
        CREATE TABLE IF NOT EXISTS joueurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            prenom TEXT,
            pseudo TEXT,
            sport TEXT,
            niveau TEXT,
            tournoi_nom TEXT
        )
    """)

    # table des equipes
    curseur.execute("""
        CREATE TABLE IF NOT EXISTS equipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            sport TEXT,
            membres TEXT,
            tournoi_nom TEXT
        )
    """)

    connexion.commit()
    connexion.close()
    print("  Base de donnees creee ou deja existante.")


# =============================================
# SAUVEGARDE
# =============================================

# cette fonction sauvegarde le tournoi dans la base de donnees
def sauvegarder_tournoi(tournoi):
    creer_base()
    connexion = sqlite3.connect(NOM_BASE)
    curseur = connexion.cursor()

    # on supprime l ancien tournoi du meme nom s il existe
    curseur.execute("DELETE FROM joueurs WHERE tournoi_nom = ?", (tournoi.nom,))
    curseur.execute("DELETE FROM equipes WHERE tournoi_nom = ?", (tournoi.nom,))
    curseur.execute("DELETE FROM tournois WHERE nom = ?", (tournoi.nom,))

    # on insere le tournoi
    curseur.execute(
        "INSERT INTO tournois (nom, tour) VALUES (?, ?)",
        (tournoi.nom, tournoi.tour)
    )

    # on insere les participants
    for p in tournoi.participants:

        # on verifie le type avec le nom de la classe
        nom_classe = type(p).__name__

        if nom_classe == "Joueur":
            curseur.execute(
                "INSERT INTO joueurs (nom, prenom, pseudo, sport, niveau, tournoi_nom) VALUES (?, ?, ?, ?, ?, ?)",
                (p.nom, p.prenom, p.pseudo, p.sport, p.niveau, tournoi.nom)
            )
        else:
            # pour une equipe on met les membres dans une chaine separee par des virgules
            membres = ""
            for j in p.joueurs:
                membres = membres + j.nom + ","

            curseur.execute(
                "INSERT INTO equipes (nom, sport, membres, tournoi_nom) VALUES (?, ?, ?, ?)",
                (p.nom, p.sport, membres, tournoi.nom)
            )

    connexion.commit()
    connexion.close()
    print("\n  Tournoi sauvegarde dans la base de donnees.")


# =============================================
# CHARGEMENT
# =============================================

# cette fonction charge le dernier tournoi sauvegarde
def charger_tournoi():
    if os.path.exists(NOM_BASE) == False:
        print("\n  Aucune base de donnees trouvee.")
        return None

    connexion = sqlite3.connect(NOM_BASE)
    curseur = connexion.cursor()

    # on recupere tous les tournois et on prend le dernier
    curseur.execute("SELECT nom, tour FROM tournois")
    tous = curseur.fetchall()

    if len(tous) == 0:
        print("\n  Aucun tournoi trouve dans la base.")
        connexion.close()
        return None

    # le dernier tournoi est le dernier de la liste
    dernier = tous[len(tous) - 1]
    nom = dernier[0]
    tour = dernier[1]

    tournoi = Tournoi(nom)
    tournoi.tour = tour

    # on recupere les joueurs de ce tournoi
    curseur.execute("SELECT nom, prenom, pseudo, sport, niveau FROM joueurs WHERE tournoi_nom = ?", (nom,))
    joueurs = curseur.fetchall()

    for j in joueurs:
        joueur = Joueur(j[0], j[1], j[2], j[3], j[4])
        tournoi.ajouter_participant(joueur)

    # on recupere les equipes de ce tournoi
    curseur.execute("SELECT nom, sport, membres FROM equipes WHERE tournoi_nom = ?", (nom,))
    equipes = curseur.fetchall()

    for e in equipes:
        nom_eq = e[0]
        sport_eq = e[1]
        membres_txt = e[2]
        joueurs_eq = []
        for nom_j in membres_txt.split(","):
            if nom_j != "":
                joueurs_eq.append(Joueur(nom_j, "", nom_j, sport_eq, "N/A"))
        eq = Equipe(nom_eq, joueurs_eq, sport_eq)
        tournoi.ajouter_participant(eq)

    connexion.close()
    print("\n  Tournoi charge depuis la base de donnees !")
    return tournoi


# =============================================
# VERIFICATION
# =============================================

# cette fonction verifie si une sauvegarde existe
def sauvegarde_existe():
    if os.path.exists(NOM_BASE) == False:
        return False

    connexion = sqlite3.connect(NOM_BASE)
    curseur = connexion.cursor()

    try:
        curseur.execute("SELECT COUNT(*) FROM tournois")
        resultat = curseur.fetchone()
        nb = resultat[0]
        connexion.close()
        if nb > 0:
            return True
        else:
            return False
    except:
        connexion.close()
        return False


# =============================================
# LISTER LES TOURNOIS
# =============================================

# cette fonction affiche tous les tournois dans la base
def lister_tournois():
    if os.path.exists(NOM_BASE) == False:
        print("  Aucune base de donnees trouvee.")
        return

    connexion = sqlite3.connect(NOM_BASE)
    curseur = connexion.cursor()

    curseur.execute("SELECT nom, tour FROM tournois")
    tournois = curseur.fetchall()
    connexion.close()

    if len(tournois) == 0:
        print("  Aucun tournoi sauvegarde.")
    else:
        print("\n  Tournois sauvegardes :")
        i = 1
        for t in tournois:
            print(f"    {i}. {t[0]} (tour {t[1]})")
            i = i + 1