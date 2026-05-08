# app.py
# fichier principal Flask
# pour lancer : python app.py
# puis ouvrir : http://localhost:5000

from flask import Flask, render_template, request, redirect, url_for, session
from Classe import Joueur, Equipe
from Match_Tournoi import Tournoi
from Persistance import sauvegarder_tournoi, charger_tournoi, sauvegarde_existe
from Sport import SPORTS_DISPONIBLES, NIVEAUX_DISPONIBLES
import random

app = Flask(__name__)
app.secret_key = "tournoi_esport_2025"

# variable globale pour le tournoi en cours
tournoi_actuel = None


# =============================================
# PAGE ACCUEIL
# =============================================
@app.route("/")
def accueil():
    sauvegarde = sauvegarde_existe()
    return render_template("accueil.html", sauvegarde=sauvegarde)


# =============================================
# NOUVEAU TOURNOI
# =============================================
@app.route("/nouveau", methods=["GET", "POST"])
def nouveau():
    if request.method == "POST":
        nom   = request.form.get("nom", "").strip()
        sport = request.form.get("sport", "").strip()
        type_p = request.form.get("type_participant", "joueurs")
        nb    = request.form.get("nb_participants", "0").strip()

        if nom == "" or sport == "":
            return render_template("nouveau.html", erreur="Remplissez tous les champs !", sports=SPORTS_DISPONIBLES)

        try:
            nb = int(nb)
            if nb < 2:
                return render_template("nouveau.html", erreur="Il faut au moins 2 participants !", sports=SPORTS_DISPONIBLES)
        except ValueError:
            return render_template("nouveau.html", erreur="Entrez un nombre valide !", sports=SPORTS_DISPONIBLES)

        session["nom_tournoi"]    = nom
        session["sport"]          = sport
        session["type_participant"] = type_p
        session["nb_participants"] = nb
        session["participants"]   = []
        session["index"]          = 0

        if type_p == "joueurs":
            return redirect(url_for("inscrire_joueur"))
        else:
            return redirect(url_for("inscrire_equipe"))

    return render_template("nouveau.html", erreur=None, sports=SPORTS_DISPONIBLES)


# =============================================
# INSCRIRE UN JOUEUR
# =============================================
@app.route("/joueur", methods=["GET", "POST"])
def inscrire_joueur():
    index = session.get("index", 0)
    nb    = session.get("nb_participants", 0)
    sport = session.get("sport", "")

    if request.method == "POST":
        nom    = request.form.get("nom", "").strip()
        prenom = request.form.get("prenom", "").strip()
        pseudo = request.form.get("pseudo", "").strip()
        niveau = request.form.get("niveau", "").strip()

        if nom == "" or prenom == "" or pseudo == "":
            return render_template("joueur.html", index=index, nb=nb, sport=sport, niveaux=NIVEAUX_DISPONIBLES, erreur="Remplissez tous les champs !")

        participants = session.get("participants", [])
        participants.append({
            "type": "joueur",
            "nom": nom, "prenom": prenom,
            "pseudo": pseudo, "sport": sport, "niveau": niveau
        })
        session["participants"] = participants
        session["index"] = index + 1

        if index + 1 < nb:
            return redirect(url_for("inscrire_joueur"))
        else:
            return redirect(url_for("creer_tournoi"))

    return render_template("joueur.html", index=index, nb=nb, sport=sport, niveaux=NIVEAUX_DISPONIBLES, erreur=None)


# =============================================
# INSCRIRE UNE EQUIPE
# =============================================
@app.route("/equipe", methods=["GET", "POST"])
def inscrire_equipe():
    index = session.get("index", 0)
    nb    = session.get("nb_participants", 0)
    sport = session.get("sport", "")

    if request.method == "POST":
        nom_eq     = request.form.get("nom_equipe", "").strip()
        membres_txt = request.form.get("membres", "").strip()

        if nom_eq == "" or membres_txt == "":
            return render_template("equipe.html", index=index, nb=nb, sport=sport, erreur="Remplissez tous les champs !")

        participants = session.get("participants", [])
        participants.append({
            "type": "equipe",
            "nom": nom_eq,
            "membres": membres_txt,
            "sport": sport
        })
        session["participants"] = participants
        session["index"] = index + 1

        if index + 1 < nb:
            return redirect(url_for("inscrire_equipe"))
        else:
            return redirect(url_for("creer_tournoi"))

    return render_template("equipe.html", index=index, nb=nb, sport=sport, erreur=None)


# =============================================
# CREER LE TOURNOI
# =============================================
@app.route("/creer")
def creer_tournoi():
    global tournoi_actuel

    nom              = session.get("nom_tournoi", "Championship")
    participants_data = session.get("participants", [])

    tournoi_actuel = Tournoi(nom)

    for pd in participants_data:
        if pd["type"] == "joueur":
            j = Joueur(pd["nom"], pd["prenom"], pd["pseudo"], pd["sport"], pd["niveau"])
            tournoi_actuel.ajouter_participant(j)
        else:
            joueurs_eq = []
            for nom_j in pd["membres"].split(","):
                nom_j = nom_j.strip()
                if nom_j != "":
                    joueurs_eq.append(Joueur(nom_j, "", nom_j, pd["sport"], "N/A"))
            eq = Equipe(pd["nom"], joueurs_eq, pd["sport"])
            tournoi_actuel.ajouter_participant(eq)

    sauvegarder_tournoi(tournoi_actuel)
    return redirect(url_for("page_tournoi"))


# =============================================
# PAGE TOURNOI
# =============================================
@app.route("/tournoi")
def page_tournoi():
    if tournoi_actuel == None:
        return redirect(url_for("accueil"))
    return render_template("tournoi.html", tournoi=tournoi_actuel)


# =============================================
# PAGE SAISIE DES SCORES
# =============================================
@app.route("/scores", methods=["GET", "POST"])
def scores():
    global tournoi_actuel

    if tournoi_actuel == None:
        return redirect(url_for("accueil"))

    if len(tournoi_actuel.participants) <= 1:
        return redirect(url_for("page_tournoi"))

    # on prepare les paires de matchs
    random.shuffle(tournoi_actuel.participants)
    liste = list(tournoi_actuel.participants)
    qualifie = None

    if len(liste) % 2 != 0:
        qualifie = liste.pop()

    matchs = []
    i = 0
    while i < len(liste):
        matchs.append({"p1": str(liste[i]), "p2": str(liste[i+1])})
        i = i + 2

    # on sauvegarde les paires en session pour les retrouver au POST
    session["matchs_tour"]  = matchs
    session["qualifie_tour"] = str(qualifie) if qualifie else None
    session["participants_tour"] = [str(p) for p in liste]

    return render_template("scores.html", matchs=matchs, qualifie=qualifie, tournoi=tournoi_actuel)


# =============================================
# VALIDER LES SCORES
# =============================================
@app.route("/valider_scores", methods=["POST"])
def valider_scores():
    global tournoi_actuel

    matchs = session.get("matchs_tour", [])
    qualifie_nom = session.get("qualifie_tour", None)
    participants_map = {str(p): p for p in tournoi_actuel.participants}

    gagnants  = []
    resultats = []
    erreur    = None

    for idx, m in enumerate(matchs):
        s1_txt = request.form.get(f"score1_{idx}", "").strip()
        s2_txt = request.form.get(f"score2_{idx}", "").strip()

        try:
            s1 = int(s1_txt)
            s2 = int(s2_txt)
        except ValueError:
            erreur = f"Entrez des scores numeriques pour le match {idx+1} !"
            return render_template("scores.html", matchs=matchs, qualifie=qualifie_nom, tournoi=tournoi_actuel, erreur=erreur)

        if s1 == s2:
            erreur = f"Egalite non autorisee pour le match {idx+1} !"
            return render_template("scores.html", matchs=matchs, qualifie=qualifie_nom, tournoi=tournoi_actuel, erreur=erreur)

        p1_obj = participants_map.get(m["p1"])
        p2_obj = participants_map.get(m["p2"])

        gagnant_obj = p1_obj if s1 > s2 else p2_obj
        gagnants.append(gagnant_obj)
        resultats.append({"p1": m["p1"], "s1": s1, "p2": m["p2"], "s2": s2, "gagnant": str(gagnant_obj)})

    # on ajoute le qualifie
    if qualifie_nom:
        for p in tournoi_actuel.participants:
            if str(p) == qualifie_nom:
                gagnants.append(p)
                break

    tournoi_actuel.participants = gagnants
    tournoi_actuel.tour         = tournoi_actuel.tour + 1
    sauvegarder_tournoi(tournoi_actuel)

    vainqueur = None
    if len(tournoi_actuel.participants) == 1:
        vainqueur = str(tournoi_actuel.participants[0])

    return render_template("resultats.html", resultats=resultats, qualifie=qualifie_nom, vainqueur=vainqueur, tournoi=tournoi_actuel)


# =============================================
# CHARGER UNE SAUVEGARDE
# =============================================
@app.route("/charger")
def charger():
    global tournoi_actuel
    tournoi_actuel = charger_tournoi()
    if tournoi_actuel != None:
        return redirect(url_for("page_tournoi"))
    return redirect(url_for("accueil"))


# on lance le serveur
app.run(debug=True)