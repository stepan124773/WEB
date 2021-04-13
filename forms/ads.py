from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class AdForm(FlaskForm):
    address = StringField('Адресс', validators=[DataRequired()])
    name = StringField("Название")
    photo_name = StringField("Фото")
    description = StringField("Описание")
    number = StringField("Номер телефона")
    submit = SubmitField('Применить')

