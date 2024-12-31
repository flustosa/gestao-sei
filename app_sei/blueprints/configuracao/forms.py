from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class FormConfig(FlaskForm):
    orgao = StringField("Número do Órgão", validators=[DataRequired()])
    sigla_orgao = StringField("Sigla do Órgão", validators=[DataRequired()])
    sigla_sistema = StringField("Sigla do Sistema", validators=[DataRequired()])
    unidade_bloqueio = StringField("Unidade de bloqueio", validators=[DataRequired()])
    token = StringField("Chave de Acesso", validators=[DataRequired()])
    validacao_processo = BooleanField("Validação do NUP")
    botao_submit = SubmitField('Enviar')
