from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class ColourForm(FlaskForm):
    colour = StringField('Colour')
    submit = SubmitField('Encrypt')