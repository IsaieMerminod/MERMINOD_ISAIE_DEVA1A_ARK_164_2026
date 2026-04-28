"""
Fichier pour gérer les formulaires avec WTForms pour les Maps.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, DataRequired

# Formulaire pour AJOUTER une map
class FormWTFAjouterMap(FlaskForm):
    nom_map_wtf = StringField("Nom de la Map", validators=[Length(min=2, max=50, message="Entre 2 et 50 caractères"), DataRequired()])
    submit = SubmitField("Enregistrer la Map")

# Formulaire pour MODIFIER une map
class FormWTFUpdateMap(FlaskForm):
    nom_map_update_wtf = StringField("Nom de la Map", validators=[Length(min=2, max=50, message="Entre 2 et 50 caractères"), DataRequired()])
    submit = SubmitField("Mettre à jour")