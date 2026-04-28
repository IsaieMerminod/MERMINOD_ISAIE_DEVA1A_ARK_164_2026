from pathlib import Path
from flask import render_template, request, flash, redirect, url_for, session
from APP_FILMS_164 import app
from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *

@app.route("/creatures_aliments_afficher/<int:id_creature_sel>", methods=['GET', 'POST'])
def creatures_aliments_afficher(id_creature_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                # Ajout du préfixe 'Creatures.' pour éviter l'ambiguïté
                strsql_creatures_aliments_afficher = """SELECT Creatures.ID_Creature, Creatures.Nom, Creatures.Torpeur_base, Creatures.Regime_alimentaire,
                                                            GROUP_CONCAT(Aliments.Nom) as AlimentsCreature FROM creature_aliment
                                                            RIGHT JOIN Creatures ON Creatures.ID_Creature = creature_aliment.ID_Creature
                                                            LEFT JOIN Aliments ON Aliments.ID_Aliment = creature_aliment.ID_Aliment
                                                            GROUP BY Creatures.ID_Creature"""
                if id_creature_sel == 0:
                    mc_afficher.execute(strsql_creatures_aliments_afficher)
                else:
                    valeur_id_creature_selected_dictionnaire = {"value_id_creature_selected": id_creature_sel}
                    # Ajout du préfixe ici aussi
                    strsql_creatures_aliments_afficher += """ HAVING Creatures.ID_Creature= %(value_id_creature_selected)s"""
                    mc_afficher.execute(strsql_creatures_aliments_afficher, valeur_id_creature_selected_dictionnaire)

                data_creatures_aliments = mc_afficher.fetchall()

                if not data_creatures_aliments and id_creature_sel == 0:
                    flash("""La table "Creatures" est vide.""", "warning")
                else:
                    flash(f"Données affichées !!", "success")

        except Exception as e:
            raise Exception(f"Erreur : {e}")

    return render_template("creatures_aliments/creatures_aliments_afficher.html", data=data_creatures_aliments)
def aliments_creatures_afficher_data(valeur_id_creature_selected_dict):
    try:
        strsql_creature_selected = """SELECT ID_Creature, Nom, Torpeur_base, Regime_alimentaire FROM Creatures WHERE ID_Creature = %(value_id_creature_selected)s"""

        strsql_aliments_non_attribues = """SELECT ID_Aliment, Nom FROM Aliments WHERE ID_Aliment NOT IN(
                                            SELECT ID_Aliment FROM creature_aliment WHERE ID_Creature = %(value_id_creature_selected)s)"""

        strsql_aliments_attribues = """SELECT Creatures.ID_Creature, Aliments.ID_Aliment, Aliments.Nom FROM creature_aliment
                                            INNER JOIN Creatures ON Creatures.ID_Creature = creature_aliment.ID_Creature
                                            INNER JOIN Aliments ON Aliments.ID_Aliment = creature_aliment.ID_Aliment
                                            WHERE Creatures.ID_Creature = %(value_id_creature_selected)s"""

        with DBconnection() as mc_afficher:
            mc_afficher.execute(strsql_aliments_non_attribues, valeur_id_creature_selected_dict)
            data_aliments_non_attribues = mc_afficher.fetchall()

            mc_afficher.execute(strsql_creature_selected, valeur_id_creature_selected_dict)
            data_creature_selected = mc_afficher.fetchall()

            mc_afficher.execute(strsql_aliments_attribues, valeur_id_creature_selected_dict)
            data_aliments_attribues = mc_afficher.fetchall()

            return data_creature_selected, data_aliments_non_attribues, data_aliments_attribues

    except Exception as e:
        raise Exception(f"Erreur data : {e}")

@app.route("/edit_aliments_creature_selected", methods=['GET', 'POST'])
def edit_aliments_creature_selected():
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                strsql_aliments_afficher = """SELECT ID_Aliment, Nom FROM Aliments ORDER BY ID_Aliment ASC"""
                mc_afficher.execute(strsql_aliments_afficher)
            data_aliments_all = mc_afficher.fetchall()

            id_creature_aliments_edit = request.values['id_creature_aliments_edit_html']
            session['session_id_creature_aliments_edit'] = id_creature_aliments_edit

            valeur_id_creature_selected_dictionnaire = {"value_id_creature_selected": id_creature_aliments_edit}

            data_creature_selected, data_aliments_non_attribues, data_aliments_attribues = aliments_creatures_afficher_data(valeur_id_creature_selected_dictionnaire)

            lst_data_aliments_non_attribues = [item['ID_Aliment'] for item in data_aliments_non_attribues]
            session['session_lst_data_aliments_non_attribues'] = lst_data_aliments_non_attribues

            lst_data_aliments_old_attribues = [item['ID_Aliment'] for item in data_aliments_attribues]
            session['session_lst_data_aliments_old_attribues'] = lst_data_aliments_old_attribues

        except Exception as e:
            raise Exception(f"Erreur edit : {e}")

    return render_template("creatures_aliments/creatures_aliments_modifier_tags_dropbox.html",
                           data_aliments=data_aliments_all,
                           data_creature_selected=data_creature_selected,
                           data_aliments_attribues=data_aliments_attribues,
                           data_aliments_non_attribues=data_aliments_non_attribues)

@app.route("/update_aliments_creature_selected", methods=['GET', 'POST'])
def update_aliments_creature_selected():
    if request.method == "POST":
        try:
            id_creature_selected = session['session_id_creature_aliments_edit']
            old_lst_data_aliments_attribues = session['session_lst_data_aliments_old_attribues']
            session.clear()

            new_lst_str_aliments = request.form.getlist('name_select_tags')
            new_lst_int_aliments = list(map(int, new_lst_str_aliments))

            lst_diff_aliments_delete = list(set(old_lst_data_aliments_attribues) - set(new_lst_int_aliments))
            lst_diff_aliments_insert = list(set(new_lst_int_aliments) - set(old_lst_data_aliments_attribues))

            strsql_insert_aliment = """INSERT INTO creature_aliment (ID_Creature, ID_Aliment) VALUES (%(value_fk_creature)s, %(value_fk_aliment)s)"""
            strsql_delete_aliment = """DELETE FROM creature_aliment WHERE ID_Aliment = %(value_fk_aliment)s AND ID_Creature = %(value_fk_creature)s"""

            with DBconnection() as mconn_bd:
                for id_aliment_ins in lst_diff_aliments_insert:
                    mconn_bd.execute(strsql_insert_aliment, {"value_fk_creature": id_creature_selected, "value_fk_aliment": id_aliment_ins})

                for id_aliment_del in lst_diff_aliments_delete:
                    mconn_bd.execute(strsql_delete_aliment, {"value_fk_creature": id_creature_selected, "value_fk_aliment": id_aliment_del})

        except Exception as e:
            raise Exception(f"Erreur update : {e}")

    return redirect(url_for('creatures_aliments_afficher', id_creature_sel=0))