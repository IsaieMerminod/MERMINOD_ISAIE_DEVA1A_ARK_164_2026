"""Démonstration d'envoi d'une requête SQL à la BD
Fichier : 2_test_connection_bd.py
Auteur : OM 2023.03.21 / Modifié pour le projet ARK
"""

from APP_FILMS_164.database.database_tools import DBconnection

try:
    """
        Une seule requête pour montrer la récupération des données de la BD en MySql.
        On va tester si on arrive à lire tes créatures (même si la table est vide).
    """
    strsql_creatures_afficher = """SELECT * FROM Creatures ORDER BY ID_Creature ASC"""

    with DBconnection() as db:
        db.execute(strsql_creatures_afficher)
        result = db.fetchall()

        print("Résultat de la table Creatures : ", result, " Type : ", type(result))


except Exception as erreur:
    print(f"2547821146 Test connection BD !"
          f"{__name__,erreur} , "
          f"{repr(erreur)}, "
          f"{type(erreur)}")