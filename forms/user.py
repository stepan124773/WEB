from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    surname = TextAreaField("Фамилия", validators=[DataRequired()])
    position = TextAreaField("Должность", validators=[DataRequired()])
    speciality = TextAreaField("Специальность", validators=[DataRequired()])
    address = TextAreaField("Адресс", validators=[DataRequired()])
    age = IntegerField("Возраст", validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')
