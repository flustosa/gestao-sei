from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class FormLogin(FlaskForm):
    usuario = StringField('Usuário', validators=[DataRequired()], description="Usuário")
    senha = PasswordField('Senha', validators=[DataRequired()], description="Senha")
    botao_submit = SubmitField('Enviar')


