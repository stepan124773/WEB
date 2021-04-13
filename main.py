from flask import redirect
from flask_login import logout_user
from data.Ad import Ad
from flask import Flask, render_template
from data import db_session
from forms.loginform import LoginForm
from forms.registerform import RegisterForm
from data.user import User
from flask_login import LoginManager, login_user, login_required
from forms.ads import AdForm

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/ads.db")
    app.run()


@app.route("/")
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(Ad)
    return render_template("index.html", news=news)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():

        number = form.number.raw_data[0]

        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.number == number).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)

            return redirect("/")

        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)

    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.number == form.number.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            address=form.address.data,
            number=form.number.data
        )
        user.set_password(form.password.data)
        user.set_modified_date()
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/add_ad', methods=['GET', 'POST'])
def add_ad():
    form = AdForm()

    if form.submit.data:
        db_sess = db_session.create_session()
        number = form.number.data
        ad = Ad(
            address=form.address.data,
            name=form.name.data,
            photo_name=form.photo_name.data,
            description=form.description.data,
            number=number,
            user_id=db_sess.query(User).filter(User.number == number).first().id

        )

        db_sess.add(ad)
        db_sess.commit()
        return redirect('/')
    return render_template('add_ad.html', form=form)


@app.route('/delete_ad/<ad_id>')
def delete_ad(ad_id):
    db_sess = db_session.create_session()
    ad = db_sess.query(Ad).get(ad_id)
    db_sess.delete(ad)
    db_sess.commit()
    return redirect('/')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    main()
