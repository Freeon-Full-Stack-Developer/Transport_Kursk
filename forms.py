from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.simple import EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):

    #Форма для регистрации нового пользователя.

    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=2, max=150)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])  # Минимальная длина пароля
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])  # Подтверждение пароля
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):

    #Форма для входа пользователя.

    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class UserInfoForm(FlaskForm):

    #Форма для редактирования информации о пользователе.

    name = StringField('Имя', validators=[DataRequired()])
    last_name = StringField('Фамилия', validators=[DataRequired()])
    email = EmailField('Электронная почта', validators=[DataRequired(), Email()])
    phone = StringField('Телефон')  # Добавлено поле для телефона
    submit = SubmitField('Сохранить')
