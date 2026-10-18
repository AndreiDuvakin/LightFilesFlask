from quart_wtf import QuartForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(QuartForm):
    username = StringField("Логин", [Length(min=4, max=25), DataRequired()])
    password = PasswordField("Пароль", [DataRequired()])
    remember_me = BooleanField("Запомнить меня")
    submit = SubmitField("Войти")
