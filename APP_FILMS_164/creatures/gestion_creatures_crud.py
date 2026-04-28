from pathlib import Path
from flask import redirect, request, session, url_for, flash, render_template
from APP_FILMS_164 import app
from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *

@app.route("/creatures_afficher/<string:order_by>/<int:id_creature_sel>", methods=['GET', 'POST'])
def creatures_afficher(order_by, id_creature_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_creature_sel == 0:
                    strsql_creatures_afficher = """SELECT ID_Creature, Nom, Torpeur_base, Regime_alimentaire FROM Creatures ORDER BY ID_Creature ASC"""
                    mc_afficher.execute(strsql_creatures_afficher)
                elif order_by == "ASC":
                    valeur_id_creature_selected_dictionnaire = {"value_id_creature_selected": id_creature_sel}
                    strsql_creatures_afficher = """SELECT ID_Creature, Nom, Torpeur_base, Regime_alimentaire FROM Creatures WHERE ID_Creature = %(value_id_creature_selected)s"""
                    mc_afficher.execute(strsql_creatures_afficher, valeur_id_creature_selected_dictionnaire)
                else:
                    strsql_creatures_afficher = """SELECT ID_Creature, Nom, Torpeur_base, Regime_alimentaire FROM Creatures ORDER BY ID_Creature DESC"""
                    mc_afficher.execute(strsql_creatures_afficher)

                data_creatures = mc_afficher.fetchall()

                if not data_creatures and id_creature_sel == 0:
                    flash("""La table "Creatures" est vide. !!""", "warning")
                elif not data_creatures and id_creature_sel > 0:
                    flash(f"La créature demandée n'existe pas !!", "warning")
                else:
                    flash(f"Données des créatures affichées !!", "success")

        except Exception as Exception_creatures_afficher:
            raise ExceptionGenresAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{creatures_afficher.__name__} ; "
                                          f"{Exception_creatures_afficher}")

    return render_template("creatures/creatures_afficher.html", data=data_creatures)

@app.route("/creatures_ajouter", methods=['GET', 'POST'])
def creatures_ajouter_wtf():
    from APP_FILMS_164.creatures.gestion_creatures_wtf_forms import FormWTFAjouterCreature
    form = FormWTFAjouterCreature()

    if request.method == "POST":
        try:
            if form.validate_on_submit():
                nom = form.nom_creature_wtf.data
                torpeur = form.torpeur_creature_wtf.data
                regime = form.regime_creature_wtf.data

                valeurs_insertion = {"value_nom": nom, "value_torpeur": torpeur, "value_regime": regime}

                strsql_insert = """INSERT INTO Creatures (ID_Creature, Nom, Torpeur_base, Regime_alimentaire) 
                                   VALUES (NULL, %(value_nom)s, %(value_torpeur)s, %(value_regime)s)"""

                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert, valeurs_insertion)

                flash(f"La créature '{nom}' a été ajoutée !", "success")
                return redirect(url_for('creatures_afficher', order_by='DESC', id_creature_sel=0))

        except Exception as e:
            raise ExceptionGenresAjouterWtf(f"Erreur lors de l'ajout : {e}")

    return render_template("creatures/creatures_ajouter.html", form=form)

@app.route("/creatures_delete", methods=['GET', 'POST'])
def creatures_delete_wtf():
    id_creature_delete = request.values.get('id_creature_btn_delete_html')

    if request.method == "POST":
        try:
            strsql_delete_creature = """DELETE FROM Creatures WHERE ID_Creature = %(value_id_creature)s"""
            valeur_delete_dictionnaire = {"value_id_creature": id_creature_delete}

            with DBconnection() as mconn_bd:
                mconn_bd.execute(strsql_delete_creature, valeur_delete_dictionnaire)

            flash(f"Créature supprimée de la base de données !!", "success")
            return redirect(url_for('creatures_afficher', order_by='ASC', id_creature_sel=0))

        except Exception as Exception_creatures_delete_wtf:
            raise ExceptionGenreDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{creatures_delete_wtf.__name__} ; "
                                            f"{Exception_creatures_delete_wtf}")

    if request.method == "GET":
        try:
            with DBconnection() as mconn_bd:
                strsql_read_creature = """SELECT ID_Creature, Nom FROM Creatures WHERE ID_Creature = %(value_id_creature)s"""
                mconn_bd.execute(strsql_read_creature, {"value_id_creature": id_creature_delete})
                data_creature_delete = mconn_bd.fetchone()

        except Exception as Exception_creatures_delete_wtf_query:
            raise ExceptionGenreDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{creatures_delete_wtf.__name__} ; "
                                            f"{Exception_creatures_delete_wtf_query}")

    return render_template("creatures/creatures_delete_wtf.html", data_delete=data_creature_delete)
@app.route("/creatures_update", methods=['GET', 'POST'])
def creatures_update_wtf():
    id_creature_update = request.values.get('id_creature_btn_edit_html')
    from APP_FILMS_164.creatures.gestion_creatures_wtf_forms import FormWTFUpdateCreature
    form_update = FormWTFUpdateCreature()

    if request.method == "POST" and form_update.submit.data:
        try:
            if form_update.validate():
                name_creature_update = form_update.nom_creature_update_wtf.data
                torpeur_update = form_update.torpeur_creature_update_wtf.data
                regime_update = form_update.regime_creature_update_wtf.data

                valeur_update_dictionnaire = {
                    "value_id_creature": id_creature_update,
                    "value_nom_creature": name_creature_update,
                    "value_torpeur": torpeur_update,
                    "value_regime": regime_update
                }

                strsql_update_creature = """UPDATE Creatures SET Nom = %(value_nom_creature)s, 
                                            Torpeur_base = %(value_torpeur)s, 
                                            Regime_alimentaire = %(value_regime)s 
                                            WHERE ID_Creature = %(value_id_creature)s"""
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_update_creature, valeur_update_dictionnaire)

                flash(f"La créature a été mise à jour !", "success")
                return redirect(url_for('creatures_afficher', order_by='ASC', id_creature_sel= 0))
        except Exception as e:
            raise Exception(f"Erreur lors de la mise à jour : {e}")

    if request.method == "GET":
        try:
            with DBconnection() as mc_select:
                strsql_select_creature = """SELECT * FROM Creatures WHERE ID_Creature = %(value_id_creature)s"""
                valeur_select_dictionnaire = {"value_id_creature": id_creature_update}
                mc_select.execute(strsql_select_creature, valeur_select_dictionnaire)
                data_creature = mc_select.fetchone()

            form_update.nom_creature_update_wtf.data = data_creature["Nom"]
            form_update.torpeur_creature_update_wtf.data = data_creature["Torpeur_base"]
            form_update.regime_creature_update_wtf.data = data_creature["Regime_alimentaire"]
        except Exception as e:
            raise Exception(f"Erreur lors de la lecture : {e}")

    return render_template("creatures/creatures_update.html", form_update=form_update)