from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  # Важно для безопасности сессий
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Используем SQLite для простоты
db = SQLAlchemy(app)

# Модель пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False) # Храним хеш пароля

    def __repr__(self):
        return f"User('{self.username}')"

# Функция для создания таблиц
def create_tables():
    db.create_all()

# Перед первым запросом создаем БД (если её нет)
with app.app_context():
    create_tables()


# Главная страница
@app.route("/")
def home():
    return render_template('home.html', user=session.get('username'))


# Страница профиля (доступна только авторизованным)
@app.route("/profile")
def profile():
    if 'username' in session:
        return render_template('profile.html', username=session['username'])
    else:
        return redirect(url_for('login'))


# Страница регистрации
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('register.html', error="Имя пользователя уже занято")

        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))  # После регистрации - на страницу логина
    return render_template('register.html')


# Страница логина
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['username'] = username
            return redirect(url_for('profile'))
        else:
            return render_template('login.html', error="Неверное имя пользователя или пароль")
    return render_template('login.html')


# Выход из системы
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
