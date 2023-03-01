from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

#Form Section
class PokemonForm(FlaskForm):
    pokemon_name = StringField('Pokemon Name', validators=[DataRequired()])
    submit = SubmitField('Submit')