from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class TypeForm(FlaskForm):
    category = StringField("Название")

    submit = SubmitField('Применить')
