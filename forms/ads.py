from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class AdForm(FlaskForm):
    address = StringField('Адрес', validators=[DataRequired()])
    name = StringField("Название")
    description = StringField("Описание")
    number = StringField("Номер телефона")
    category = StringField("Категория")
    submit = SubmitField('Применить')
