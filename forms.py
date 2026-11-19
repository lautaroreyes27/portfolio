from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired(), Length(max=50)])
    password = PasswordField("Contraseña", validators=[DataRequired()])


class PerfilForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=100)])
    titulo = StringField("Título", validators=[DataRequired(), Length(max=150)])
    bio = TextAreaField("Presentación", validators=[DataRequired()])
    email = StringField("Email", validators=[Length(max=120)])
    github = StringField("GitHub (URL)", validators=[Length(max=150)])
    linkedin = StringField("LinkedIn (URL)", validators=[Length(max=150)])
