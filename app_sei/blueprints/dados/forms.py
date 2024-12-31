from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError
from app_sei.blueprints.configuracao.models import Config


class FormBloqueio(FlaskForm):
    processo = StringField('Número do processo', validators=[DataRequired()],
                           render_kw={"placeholder": "00000.000000/0000-00"})
    motivo = StringField('Motivo', validators=[DataRequired()])
    operacao = SelectField("Operação", choices=[(1, "Bloqueio"), (2, "Desbloqueio")])
    botao_submit = SubmitField('Enviar')

    def validate_processo(self, processo):
        """Validação do formato dos processo 00000.000000/2024-00"""
        config = Config.query.get(1)
        if config.valida_processo:
            processo_parse = processo.data.replace(".", "").replace("-", "").replace(' ', '').replace('/', '').strip()
            if len(processo_parse) != 17 or processo_parse.isnumeric() is False:
                raise ValidationError('Insira corretamente o número do processo com 17 dígitos!')
        else:
            pass

    def validate_motivo(self, motivo):
        """Validação do motivo do bloqueio/desbloqueio, no mínimo 5 caracteres"""
        if len(motivo.data.replace(' ', '')) < 5:
            raise ValidationError('Preencha o motivo com pelo menos 5 caracteres')


class FormLote(FlaskForm):
    arquivo = FileField('Browse...', validators=[FileRequired(), FileAllowed(['txt'])])
    motivo = StringField('Motivo', validators=[DataRequired()])
    operacao = SelectField("Operação", choices=[(1, "Bloqueio"), (2, "Desbloqueio")])
    botao_submit = SubmitField('Enviar')

    def validate_motivo(self, motivo):
        """Validação do motivo do bloqueio/desbloqueio, no mínimo 5 caracteres"""
        if len(motivo.data.replace(' ', '')) < 5:
            raise ValidationError('Preencha o motivo com pelo menos 5 caracteres')
