from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms import LoginForm, RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash

# Создание экземпляра Flask и настройка базы данных
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Инициализация менеджера сессий для пользователей
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Модель пользователя для базы данных
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150))  # Имя пользователя
    last_name = db.Column(db.String(150))  # Фамилия пользователя
    email = db.Column(db.String(150), unique=True)  # Email пользователя
    phone = db.Column(db.String(50))  # Телефон пользователя

# Загрузка пользователя по ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Главная страница
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

# Регистрация пользователя
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter((User .username == form.username.data) | (User .email == form.email.data)).first()
        if existing_user:
            flash('Пользователь с таким email или именем пользователя уже существует.', 'error')
            return redirect(url_for('register'))

        # Хеширование пароля перед сохранением
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        user = User(username=form.username.data, password=hashed_password, email=form.email.data)

        db.session.add(user)
        db.session.commit()
        flash('Регистрация прошла успешно!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Страница входа
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('lk'))
        else:
            flash('Не удалось войти. Пожалуйста, проверьте логин и пароль.', 'danger')
    return render_template('login.html', form=form)

# Личный кабинет
@app.route('/lk')
@login_required
def lk():
    return render_template('lk.html')

# Редактирование профиля
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        # Получаем данные из формы
        current_user.name = request.form['name']
        current_user.last_name = request.form['last_name']
        current_user.email = request.form['email']
        current_user.phone = request.form['phone']

        # Сохраните изменения в базе данных
        db.session.commit()
        flash('Ваш профиль был обновлён!', 'success')
        return redirect(url_for('lk'))

    return render_template('edit_profile.html')  # Возвращаем шаблон для редактирования профиля

# Страница работы
@app.route('/work')
def work():
    return render_template('work.html')

# Страница информации
@app.route('/history')
def history():
    return render_template('history.html')

# Страница онлайн автобусов
@app.route('/bus_online')
@login_required
def bus_online():
    return render_template('bus_online.html')

# Выход пользователя
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Создание базы данных и таблиц
with app.app_context():
    db.create_all()

# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)

