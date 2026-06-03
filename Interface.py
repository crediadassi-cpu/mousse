# interface.py
# interface graphique avec Tkinter
# pour lancer : python interface.py

import tkinter as tk
from tkinter import ttk, messagebox
from Classe import Joueur, Equipe
from Match_Tournoi import Tournoi
from Persistance import sauvegarder_tournoi, charger_tournoi, sauvegarde_existe
from Sport import SPORTS_DISPONIBLES, NIVEAUX_DISPONIBLES
import random

# =============================================
# CREATION DE LA FENETRE PRINCIPALE
# =============================================
fenetre = tk.Tk()
fenetre.title("Gestionnaire de Tournoi")
fenetre.geometry("500x500")
fenetre.configure(bg="white")

# =============================================
# VARIABLES GLOBALES
# =============================================
# ces variables servent a garder les donnees entre les pages
tournoi_actuel          = None
nom_tournoi_global      = ""
sport_global            = ""
nb_joueurs_global       = 0
joueurs_inscrits_global = []
index_joueur_global     = 0

# champs du formulaire nouveau tournoi
entry_nom_tournoi  = None
entry_nb_joueurs   = None
combo_sport_global = None

# champs du formulaire inscription joueur
entry_nom_j    = None
entry_prenom_j = None
entry_pseudo_j = None
combo_niveau_j = None


# =============================================
# FONCTION POUR VIDER LA FENETRE
# =============================================
def vider():
    # on supprime tous les widgets de la fenetre
    for widget in fenetre.winfo_children():
        widget.destroy()


# =============================================
# PAGE ACCUEIL
# =============================================
def page_accueil():
    vider()

    # titre
    tk.Label(fenetre, text="GESTIONNAIRE DE TOURNOI",
        font=("Arial", 16, "bold"), bg="white", fg="black").pack(pady=30)

    # description
    tk.Label(fenetre, text="Bienvenue ! Choisissez une option.",
        font=("Arial", 11), bg="white", fg="gray").pack(pady=5)

    # bouton nouveau tournoi
    tk.Button(fenetre, text="Nouveau Tournoi",
        command=page_formulaire,
        font=("Arial", 12), bg="black", fg="white",
        width=20, pady=8).pack(pady=10)

    # bouton charger sauvegarde - affiche seulement si une sauvegarde existe
    if sauvegarde_existe():
        tk.Button(fenetre, text="Charger Sauvegarde",
            command=charger,
            font=("Arial", 12), bg="gray", fg="white",
            width=20, pady=8).pack(pady=5)

    # bouton quitter
    tk.Button(fenetre, text="Quitter",
        command=fenetre.quit,
        font=("Arial", 12), bg="white", fg="gray",
        width=20, pady=8).pack(pady=5)


# =============================================
# PAGE FORMULAIRE NOUVEAU TOURNOI
# =============================================
def page_formulaire():
    global entry_nom_tournoi, entry_nb_joueurs, combo_sport_global
    vider()

    # titre
    tk.Label(fenetre, text="NOUVEAU TOURNOI",
        font=("Arial", 16, "bold"), bg="white", fg="black").pack(pady=20)

    # champ nom du tournoi
    tk.Label(fenetre, text="Nom du tournoi :",
        font=("Arial", 11), bg="white").pack()
    entry_nom_tournoi = tk.Entry(fenetre, font=("Arial", 12), width=30)
    entry_nom_tournoi.pack(pady=5)

    # liste deroulante pour le sport
    tk.Label(fenetre, text="Sport :",
        font=("Arial", 11), bg="white").pack()
    combo_sport_global = ttk.Combobox(fenetre,
        values=SPORTS_DISPONIBLES, state="readonly",
        font=("Arial", 11), width=28)
    combo_sport_global.current(0)
    combo_sport_global.pack(pady=5)

    # champ nombre de joueurs
    tk.Label(fenetre, text="Nombre de joueurs :",
        font=("Arial", 11), bg="white").pack()
    entry_nb_joueurs = tk.Entry(fenetre, font=("Arial", 12), width=30)
    entry_nb_joueurs.pack(pady=5)

    # boutons
    tk.Button(fenetre, text="Suivant",
        command=valider_formulaire,
        font=("Arial", 12), bg="black", fg="white",
        width=20, pady=8).pack(pady=15)

    tk.Button(fenetre, text="Retour",
        command=page_accueil,
        font=("Arial", 11), bg="white", fg="gray",
        width=20).pack()


def valider_formulaire():
    global nom_tournoi_global, sport_global, nb_joueurs_global
    global joueurs_inscrits_global, index_joueur_global

    # on lit les valeurs des champs
    nom   = entry_nom_tournoi.get().strip()
    sport = combo_sport_global.get()

    # verification nom
    if nom == "":
        messagebox.showerror("Erreur", "Entrez un nom de tournoi !")
        return

    # verification nombre de joueurs
    try:
        nb = int(entry_nb_joueurs.get())
        if nb < 2:
            messagebox.showerror("Erreur", "Il faut au moins 2 joueurs !")
            return
    except ValueError:
        messagebox.showerror("Erreur", "Entrez un nombre valide !")
        return

    # on sauvegarde dans les variables globales
    nom_tournoi_global      = nom
    sport_global            = sport
    nb_joueurs_global       = nb
    joueurs_inscrits_global = []
    index_joueur_global     = 0

    # on passe a l inscription des joueurs
    page_inscrire_joueur()


# =============================================
# PAGE INSCRIPTION JOUEUR
# =============================================
def page_inscrire_joueur():
    global entry_nom_j, entry_prenom_j, entry_pseudo_j, combo_niveau_j
    vider()

    # titre avec progression
    tk.Label(fenetre,
        text=f"JOUEUR {index_joueur_global + 1} / {nb_joueurs_global}",
        font=("Arial", 16, "bold"), bg="white", fg="black").pack(pady=15)

    # sport affiche en lecture seule
    tk.Label(fenetre, text=f"Sport : {sport_global}",
        font=("Arial", 11), bg="white", fg="gray").pack(pady=3)

    # champ nom
    tk.Label(fenetre, text="Nom :",
        font=("Arial", 11), bg="white").pack()
    entry_nom_j = tk.Entry(fenetre, font=("Arial", 12), width=30)
    entry_nom_j.pack(pady=4)

    # champ prenom
    tk.Label(fenetre, text="Prenom :",
        font=("Arial", 11), bg="white").pack()
    entry_prenom_j = tk.Entry(fenetre, font=("Arial", 12), width=30)
    entry_prenom_j.pack(pady=4)

    # champ pseudo
    tk.Label(fenetre, text="Pseudo :",
        font=("Arial", 11), bg="white").pack()
    entry_pseudo_j = tk.Entry(fenetre, font=("Arial", 12), width=30)
    entry_pseudo_j.pack(pady=4)

    # liste deroulante pour le niveau
    tk.Label(fenetre, text="Niveau :",
        font=("Arial", 11), bg="white").pack()
    combo_niveau_j = ttk.Combobox(fenetre,
        values=NIVEAUX_DISPONIBLES, state="readonly",
        font=("Arial", 11), width=28)
    combo_niveau_j.current(0)
    combo_niveau_j.pack(pady=4)

    # bouton suivant ou terminer selon si c est le dernier joueur
    if index_joueur_global < nb_joueurs_global - 1:
        texte_btn = "Joueur suivant"
    else:
        texte_btn = "Terminer"

    tk.Button(fenetre, text=texte_btn,
        command=valider_joueur,
        font=("Arial", 12), bg="black", fg="white",
        width=20, pady=8).pack(pady=12)


def valider_joueur():
    global tournoi_actuel, joueurs_inscrits_global, index_joueur_global

    # on lit les valeurs des champs
    nom    = entry_nom_j.get().strip()
    prenom = entry_prenom_j.get().strip()
    pseudo = entry_pseudo_j.get().strip()
    niveau = combo_niveau_j.get()

    # verification que tous les champs sont remplis
    if nom == "" or prenom == "" or pseudo == "":
        messagebox.showerror("Erreur", "Remplissez tous les champs !")
        return

    # on cree le joueur et on l ajoute a la liste
    j = Joueur(nom, prenom, pseudo, sport_global, niveau)
    joueurs_inscrits_global.append(j)
    index_joueur_global = index_joueur_global + 1

    # si tous les joueurs sont inscrits on cree le tournoi
    if index_joueur_global < nb_joueurs_global:
        page_inscrire_joueur()
    else:
        tournoi_actuel = Tournoi(nom_tournoi_global)
        for j in joueurs_inscrits_global:
            tournoi_actuel.ajouter_participant(j)
        sauvegarder_tournoi(tournoi_actuel)
        page_tournoi()


# =============================================
# PAGE TOURNOI
# =============================================
def page_tournoi():
    vider()

    # titre
    tk.Label(fenetre, text=tournoi_actuel.nom.upper(),
        font=("Arial", 16, "bold"), bg="white", fg="black").pack(pady=15)

    tk.Label(fenetre,
        text=f"Tour {tournoi_actuel.tour}  |  {len(tournoi_actuel.participants)} participant(s)",
        font=("Arial", 11), bg="white", fg="gray").pack(pady=3)

    # liste des participants
    tk.Label(fenetre, text="Participants :",
        font=("Arial", 11, "bold"), bg="white").pack(pady=(10, 3))

    i = 1
    for p in tournoi_actuel.participants:
        tk.Label(fenetre, text=f"  {i}.  {p}",
            font=("Arial", 11), bg="white", fg="black").pack(anchor="w", padx=60)
        i = i + 1

    # bouton jouer
    tk.Button(fenetre, text="Jouer le Tour",
        command=jouer_tour_auto,
        font=("Arial", 12), bg="black", fg="white",
        width=20, pady=8).pack(pady=20)

    tk.Button(fenetre, text="Retour Accueil",
        command=page_accueil,
        font=("Arial", 11), bg="white", fg="gray",
        width=20).pack()


# =============================================
# JOUER UN TOUR EN MODE AUTOMATIQUE
# =============================================
def jouer_tour_auto():
    global tournoi_actuel

    # si il reste 1 seul joueur c est le vainqueur
    if len(tournoi_actuel.participants) <= 1:
        messagebox.showinfo("Fin", f"Vainqueur : {tournoi_actuel.participants[0]}")
        return

    vider()

    # titre
    tk.Label(fenetre, text=f"TOUR {tournoi_actuel.tour}",
        font=("Arial", 16, "bold"), bg="white", fg="black").pack(pady=15)

    tk.Label(fenetre, text="Resultats des matchs :",
        font=("Arial", 11, "bold"), bg="white").pack(pady=5)

    # on melange les participants
    random.shuffle(tournoi_actuel.participants)
    gagnants  = []
    resultats = []

    qualifie = None
    liste    = list(tournoi_actuel.participants)

    # si nombre impair un joueur passe automatiquement
    if len(liste) % 2 != 0:
        qualifie = liste.pop()

    # on joue les matchs deux par deux
    i = 0
    while i < len(liste):
        p1 = liste[i]
        p2 = liste[i + 1]

        # scores aleatoires
        s1 = random.randint(0, 10)
        s2 = random.randint(0, 10)
        while s1 == s2:
            s2 = random.randint(0, 10)

        # on determine le gagnant
        if s1 > s2:
            gagnant = p1
        else:
            gagnant = p2

        gagnants.append(gagnant)
        resultats.append((p1, s1, p2, s2, gagnant))
        i = i + 2

    # on ajoute le joueur qui passe automatiquement
    if qualifie != None:
        gagnants.append(qualifie)

    # on affiche les resultats
    for p1, s1, p2, s2, gagnant in resultats:
        texte = f"{p1}  [{s1} - {s2}]  {p2}   =>  {gagnant}"
        tk.Label(fenetre, text=texte,
            font=("Arial", 10), bg="white", fg="black").pack(pady=2)

    if qualifie != None:
        tk.Label(fenetre, text=f"{qualifie} : BYE (passe automatiquement)",
            font=("Arial", 10), bg="white", fg="gray").pack(pady=2)

    # on met a jour le tournoi
    tournoi_actuel.participants = gagnants
    tournoi_actuel.tour         = tournoi_actuel.tour + 1
    sauvegarder_tournoi(tournoi_actuel)

    # si il reste 1 joueur c est le vainqueur final
    if len(tournoi_actuel.participants) == 1:
        vainqueur = tournoi_actuel.participants[0]
        tk.Label(fenetre, text=f"VAINQUEUR : {vainqueur}",
            font=("Arial", 14, "bold"), bg="white", fg="black").pack(pady=15)
        tk.Button(fenetre, text="Retour Accueil",
            command=page_accueil,
            font=("Arial", 12), bg="black", fg="white",
            width=20, pady=8).pack(pady=10)
    else:
        tk.Button(fenetre, text="Tour suivant",
            command=jouer_tour_auto,
            font=("Arial", 12), bg="black", fg="white",
            width=20, pady=8).pack(pady=10)
        tk.Button(fenetre, text="Retour Accueil",
            command=page_accueil,
            font=("Arial", 11), bg="white", fg="gray",
            width=20).pack()


# =============================================
# CHARGER UNE SAUVEGARDE
# =============================================
def charger():
    global tournoi_actuel
    tournoi_actuel = charger_tournoi()
    if tournoi_actuel != None:
        page_tournoi()
    else:
        messagebox.showerror("Erreur", "Impossible de charger la sauvegarde.")


# =============================================
# LANCEMENT DE L APPLICATION
# =============================================
page_accueil()
fenetre.mainloop()