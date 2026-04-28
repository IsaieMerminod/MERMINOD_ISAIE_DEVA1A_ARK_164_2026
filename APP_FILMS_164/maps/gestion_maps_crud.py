from pathlib import Path
from flask import redirect, request, session, url_for, flash, render_template
from APP_FILMS_164 import app
from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *

@app.route("/maps_afficher/<string:order_by>/<int:id_map_sel>", methods=['GET', 'POST'])
def maps_afficher(order_by, id_map_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_map_sel == 0:
                    strsql_maps_afficher = """SELECT ID_Map, Nom_map FROM Maps ORDER BY ID_Map ASC"""
                    mc_afficher.execute(strsql_maps_afficher)
                elif order_by == "ASC":
                    valeur_id_map_selected_dictionnaire = {"value_id_map_selected": id_map_sel}
                    strsql_maps_afficher = """SELECT ID_Map, Nom_map FROM Maps WHERE ID_Map = %(value_id_map_selected)s"""
                    mc_afficher.execute(strsql_maps_afficher, valeur_id_map_selected_dictionnaire)
                else:
                    strsql_maps_afficher = """SELECT ID_Map, Nom_map FROM Maps ORDER BY ID_Map DESC"""
                    mc_afficher.execute(strsql_maps_afficher)

                data_maps = mc_afficher.fetchall()

                if not data_maps and id_map_sel == 0:
                    flash("""La table "Maps" est vide.""", "warning")
                else:
                    flash(f"Données des maps affichées !!", "success")

        except Exception as e:
            raise Exception(f"Erreur afficher maps : {e}")

    return render_template("maps/maps_afficher.html", data=data_maps)

@app.route("/maps_ajouter", methods=['GET', 'POST'])
def maps_ajouter_wtf():
    from APP_FILMS_164.maps.gestion_maps_wtf_forms import FormWTFAjouterMap
    form = FormWTFAjouterMap()

    if request.method == "POST":
        try:
            if form.validate_on_submit():
                nom = form.nom_map_wtf.data
                valeurs_insertion = {"value_nom": nom}
                strsql_insert = """INSERT INTO Maps (ID_Map, Nom_map) VALUES (NULL, %(value_nom)s)"""

                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert, valeurs_insertion)

                flash(f"La map '{nom}' a été ajoutée !", "success")
                return redirect(url_for('maps_afficher', order_by='ASC', id_map_sel=0))

        except Exception as e:
            raise Exception(f"Erreur ajouter map : {e}")

    return render_template("maps/maps_ajouter.html", form=form)

@app.route("/maps_update", methods=['GET', 'POST'])
def maps_update_wtf():
    id_map_update = request.values.get('id_map_btn_edit_html')
    from APP_FILMS_164.maps.gestion_maps_wtf_forms import FormWTFUpdateMap
    form_update = FormWTFUpdateMap()

    if request.method == "POST" and form_update.submit.data:
        try:
            if form_update.validate():
                nom = form_update.nom_map_update_wtf.data
                valeur_update = {"value_id": id_map_update, "value_nom": nom}
                strsql_update = """UPDATE Maps SET Nom_map = %(value_nom)s WHERE ID_Map = %(value_id)s"""

                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_update, valeur_update)

                flash(f"La map a été mise à jour !", "success")
                return redirect(url_for('maps_afficher', order_by='ASC', id_map_sel=0))
        except Exception as e:
            raise Exception(f"Erreur update map : {e}")

    if request.method == "GET":
        try:
            with DBconnection() as mc_select:
                strsql_select = """SELECT * FROM Maps WHERE ID_Map = %(value_id)s"""
                mc_select.execute(strsql_select, {"value_id": id_map_update})
                data_map = mc_select.fetchone()
            form_update.nom_map_update_wtf.data = data_map["Nom_map"]
        except Exception as e:
            raise Exception(f"Erreur lecture map : {e}")

    return render_template("maps/maps_update.html", form_update=form_update)

@app.route("/maps_delete", methods=['GET', 'POST'])
def maps_delete_wtf():
    id_map_delete = request.values.get('id_map_btn_delete_html')

    if request.method == "POST":
        try:
            strsql_delete = """DELETE FROM Maps WHERE ID_Map = %(value_id)s"""
            with DBconnection() as mconn_bd:
                mconn_bd.execute(strsql_delete, {"value_id": id_map_delete})

            flash(f"Map supprimée !", "success")
            return redirect(url_for('maps_afficher', order_by='ASC', id_map_sel=0))
        except Exception as e:
            raise Exception(f"Erreur delete map : {e}")

    if request.method == "GET":
        try:
            with DBconnection() as mconn_bd:
                strsql_read = """SELECT ID_Map, Nom_map FROM Maps WHERE ID_Map = %(value_id)s"""
                mconn_bd.execute(strsql_read, {"value_id": id_map_delete})
                data_map_delete = mconn_bd.fetchone()
        except Exception as e:
            raise Exception(f"Erreur lecture delete map : {e}")

    return render_template("maps/maps_delete_wtf.html", data_delete=data_map_delete)