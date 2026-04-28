from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import Length, DataRequired

class FormWTFAjouterCreature(FlaskForm):
    nom_creature_wtf = StringField("Nom de la créature", validators=[Length(min=2, max=50), DataRequired()])
    torpeur_creature_wtf = IntegerField("Torpeur de base", validators=[DataRequired()])
    regime_creature_wtf = StringField("Régime alimentaire", validators=[DataRequired()])
    submit = SubmitField("Enregistrer la créature")

class FormWTFUpdateCreature(FlaskForm):
    nom_creature_update_wtf = StringField("Nom de la créature", validators=[Length(min=2, max=50), DataRequired()])
    torpeur_creature_update_wtf = IntegerField("Torpeur de base", validators=[DataRequired()])
    regime_creature_update_wtf = StringField("Régime alimentaire", validators=[DataRequired()])
    submit = SubmitField("Mettre à jour")