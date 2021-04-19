from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    password = PasswordField('Пароль(его надо будет запомнить)', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    number = StringField('Номер телефона', validators=[DataRequired()])

    submit = SubmitField('Зарегистрироваться')
