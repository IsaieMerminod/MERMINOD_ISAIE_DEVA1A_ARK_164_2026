"""Gestion des "routes" FLASK et des données pour les créatures ARK.
Fichier : gestion_genres_crud.py (Adapté pour ARK)
"""
from pathlib import Path
from flask import redirect, request, session, url_for, flash, render_template
from APP_FILMS_164 import app
from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *

@app.route("/genres_afficher/<string:order_by>/<int:id_genre_sel>", methods=['GET', 'POST'])
def genres_afficher(order_by, id_genre_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                # 1. CAS : Affichage TOUT par ordre croissant
                if order_by == "ASC" and id_genre_sel == 0:
                    strsql_genres_afficher = """SELECT ID_Creature, Nom, Torpeur_base, Regime_alimentaire FROM Creatures ORDER BY ID_Creature ASC"""
                    mc_afficher.execute(strsql_genres_afficher)

                # 2. CAS : Affichage d'une seule créature précise
                elif order_by == "ASC":
                    valeur_id_genre_selected_dictionnaire = {"value_id_genre_selected": id_genre_sel}
                    strsql_genres_afficher = """SELECT ID_Creature, Nom, Torpeur_base, Regime_alimentaire FROM Creatures WHERE ID_Creature = %(value_id_genre_selected)s"""
                    mc_afficher.execute(strsql_genres_afficher, valeur_id_genre_selected_dictionnaire)

                # 3. CAS : Affichage TOUT par ordre décroissant
                else:
                    strsql_genres_afficher = """SELECT ID_Creature, Nom, Torpeur_base, Regime_alimentaire FROM Creatures ORDER BY ID_Creature DESC"""
                    mc_afficher.execute(strsql_genres_afficher)

                data_genres = mc_afficher.fetchall()

                # Messages de retour pour l'utilisateur
                if not data_genres and id_genre_sel == 0:
                    flash("""La table "Creatures" est vide. !!""", "warning")
                elif not data_genres and id_genre_sel > 0:
                    flash(f"La créature demandée n'existe pas !!", "warning")
                else:
                    flash(f"Données des créatures affichées !!", "success")

        except Exception as Exception_genres_afficher:
            raise ExceptionGenresAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{genres_afficher.__name__} ; "
                                          f"{Exception_genres_afficher}")

    return render_template("genres/maps_afficher.html", data=data_genres)

@app.route("/genres_ajouter", methods=['GET', 'POST'])
def genres_ajouter_wtf():
    # Note : Il faudra aussi modifier FormWTFAjouterGenres dans gestion_genres_wtf_forms.py
    from APP_FILMS_164.genres.gestion_genres_wtf_forms import FormWTFAjouterGenres
    form = FormWTFAjouterGenres()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                name_creature = form.nom_genre_wtf.data # On garde le nom du champ du prof pour l'instant
                valeurs_insertion_dictionnaire = {"value_nom": name_creature}

                # On insère dans TA table
                strsql_insert_genre = """INSERT INTO Creatures (ID_Creature, Nom) VALUES (NULL, %(value_nom)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_genre, valeurs_insertion_dictionnaire)

                flash(f"Créature ajoutée !!", "success")
                return redirect(url_for('genres_afficher', order_by='DESC', id_genre_sel=0))

        except Exception as Exception_genres_ajouter_wtf:
            raise ExceptionGenresAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{genres_ajouter_wtf.__name__} ; "
                                            f"{Exception_genres_ajouter_wtf}")

    return render_template("genres/maps_ajouter.html", form=form)