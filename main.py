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
from flask import request, url_for
from data.categories import Categories
from forms.typeform import TypeForm
import flask_login
from way import way

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/ads.db")
    app.run()


@app.route("/", methods=['GET', 'POST'])
def index():
    form = TypeForm()
    db_sess = db_session.create_session()

    ads = db_sess.query(Ad)

    if flask_login.current_user.is_authenticated:
        ads = sorted(ads, key=lambda x: way(x.address, flask_login.current_user.address))

    categ = db_sess.query(Categories)
    if form.submit.data:
        if form.category.data:
            if form.category.data == "999":
                return render_template("index.html", ads=ads, categ=categ, form=form, cat="Любая категория")
            cat = db_sess.query(Categories).filter(Categories.id == int(form.category.data)).first().title
            return render_template("index.html", ads=ads, categ=categ, form=form, cat=cat)
    return render_template("index.html", ads=ads, categ=categ, form=form, cat="Любая категория")


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
    db_sess = db_session.create_session()
    categories = db_sess.query(Categories).all()
    if form.submit.data:

        number = form.number.data
        if db_sess.query(User).filter(User.number == number).first():

            ad = Ad(
                address=form.address.data,
                name=form.name.data,
                category=db_sess.query(Categories).filter(Categories.id == form.category.data).first().title,
                description=form.description.data,
                number=number,
                user_id=db_sess.query(User).filter(User.number == number).first().id
            )

            db_sess.add(ad)
            db_sess.commit()
        else:
            return render_template('add_ad.html',
                                   form=form,
                                   message="Вы указали не тот номер телефона")

        return redirect('/add_photo')
    return render_template('add_ad.html', form=form, cate=categories)


@app.route('/add_photo', methods=['POST', 'GET'])
def add_photo():
    db_sess = db_session.create_session()
    ads = db_sess.query(Ad).all()
    n = 0
    for ad in ads:
        if ad.id > n:
            n = ad.id
    ad = db_sess.query(Ad).filter(Ad.id == n).first()

    if request.method == 'GET':

        return f'''<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                            <link rel="stylesheet"
                            href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                            integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                            crossorigin="anonymous">
                            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                            <title>Отбор астронавтов</title>
                          </head>
                          <body>
                            <h1>А теперь выберите фото вашей вещи</h1>
                            <form method="post" enctype="multipart/form-data">
                               <div class="form-group">
                                    <label for="photo">Выберите фото</label>
                                    <input type="file" class="form-control-file" id="photo" name="file">
                                </div>
                                <button type="submit" class="btn btn-primary">Отправить</button>
                            </form>
                          </body>
                        </html>'''
    elif request.method == 'POST':

        f = request.files['file']
        from PIL import Image
        im = Image.open(f).resize((300, 300))
        im.save(f'static/img/{str(ad.id)}.jpg')
        ad.photo_name = str(ad.id)
        db_sess.commit()
        return redirect('/')


@app.route('/delete_ad/<ad_id>')
def delete_ad(ad_id):
    db_sess = db_session.create_session()
    ad = db_sess.query(Ad).get(ad_id)
    db_sess.delete(ad)
    db_sess.commit()
    return redirect('/')


@app.route('/edit_ad/<id>', methods=['GET', 'POST'])
def dep_ad(id):
    form = AdForm()

    if request.method == "GET":
        db_sess = db_session.create_session()
        ad = db_sess.query(Ad).filter(Ad.id == id).first()
        if ad:
            form.address.data = ad.address
            form.name.data = ad.name
            form.category.data = ad.category
            form.description.data = ad.description
            form.number.data = "Если хотите сменить номер, то зарегистрируйтесь заново"

    if form.submit.data:

        db_sess = db_session.create_session()
        ad = db_sess.query(Ad).filter(Ad.id == id).first()

        if ad:
            ad.name = form.name.data
            ad.address = form.address.data
            ad.category = db_sess.query(Categories).filter(Categories.id == form.category.data).first().title
            ad.description = form.description.data

            db_sess.commit()

            return redirect('/')

    categ = db_sess.query(Categories)
    return render_template('add_ad.html',
                           title='Редактирование работы',
                           form=form, cate=categ
                           )


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    main()
