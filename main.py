from flask_login import LoginManager
from data.Ad import Ad
from flask import Flask, render_template
from data import db_session
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

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
if __name__ == '__main__':
    main()
