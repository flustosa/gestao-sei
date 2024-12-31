from flask import render_template, flash, redirect, Blueprint, url_for, session, helpers
from app_sei.blueprints.bloqueio.forms import FormBloqueio
from app_sei.blueprints.bloqueio.functions.bloqueio import bloquear_processo, desbloquear_processo
from app_sei.blueprints.configuracao.models import Config
from app_sei.blueprints.login.routes import login_required
from dotenv import load_dotenv
import os

bloqueio = Blueprint('bloqueio', __name__, template_folder='templates')

root_path = helpers.get_root_path('app')
load_dotenv(os.path.join(root_path, '.env'))
url = os.getenv('URL_WSSEI')


@bloqueio.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Função de bloqueio/desbloqueio de processos, usa o ws SOAP do SEI"""
    config_params = Config.query.get(1)
    sigla_sistema = config_params.sigla_sistema
    token = config_params.token
    unidade = config_params.unidade_bloqueio
    form = FormBloqueio()
    motivo = form.motivo.data
    processo = form.processo.data

    usuario = session['usuario']['sigla_usuario']

    if form.validate_on_submit() and form.operacao.data == "1":
        try:
            bloquear = bloquear_processo(sigla_sistema, token, unidade, processo, url, motivo, usuario)
            if bloquear[1] == 1:
                flash(f'{bloquear[0]}', 'alert-danger')
            elif bloquear[1] == 0:
                flash(f'{bloquear[0]}', 'alert-success')
            else:
                flash(f'Erro desconhecido: {bloquear}', 'alert-danger')
        finally:
            form = FormBloqueio(formdata=None)
            redirect(url_for('bloqueio.index'))

    elif form.validate_on_submit() and form.operacao.data == "2":
        try:
            desbloquear = desbloquear_processo(sigla_sistema, token, unidade, processo, url, motivo, usuario)
            if desbloquear[1] == 1:
                flash(f'{desbloquear[0]}', 'alert-danger')
            elif desbloquear[1] == 0:
                flash(f'{desbloquear[0]}', 'alert-success')
            else:
                flash(f'Erro desconhecido: {desbloquear[0]}', 'alert-danger')
        finally:
            form = FormBloqueio(formdata=None)
            redirect(url_for('bloqueio.index'))

    return render_template("bloqueio/index.html", form=form)
