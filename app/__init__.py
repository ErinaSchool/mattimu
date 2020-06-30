# モジュールインポート
from flask import Flask, render_template
# データベースを利用するために追加
from flask_sqlalchemy import SQLAlchemy
# flaks-loginのライブラリ追加
from flask_login import LoginManager

# Flaskアプリの生成
app = Flask(__name__)

# ここから /// データベースの設定
app.secret_key = "super secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///qa-site.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# ここまで /// データベースの設定

# sqlalchemyを通してflaskからdbアクセスをするための入り口
db = SQLAlchemy(app)

# flask-loginに関する設定
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

# データベースのimport
from app.models.user import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# authに関するルーティングを追加
from app.views.auth import auth

# authに関するルートをflaskアプリであるappに追加
app.register_blueprint(auth)
from app.views.questions import questions

app.register_blueprint(auth)
# url_prefixに「/questions」を入れると
# http://localhost:5000/questions/ というリンクになりわかりやすくなるので設定を追加しました
app.register_blueprint(questions, url_prefix='/questions')


# indexのルート設定
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mypageshow.html')
def mypageshow():
    return render_template('mypage/mypageshow.html')

@app.route('/free.html')
def free():
    return render_template('free.html')

@app.route('/rate.html')
def rate():
    return render_template('rate.html')

@app.route('/mypageupdate.html')
def mypageupdate():
    return render_template('mypage/mypageupdate.html')