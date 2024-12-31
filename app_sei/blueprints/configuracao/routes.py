from flask import Blueprint, render_template, url_for, flash, redirect, request
from app_sei.blueprints.configuracao.forms import FormConfig
from app_sei.blueprints.configuracao.models import Config
from app_sei.blueprints.login.routes import login_required
from app_sei.app import db

configuracao = Blueprint('configuracao', __name__, template_folder='templates')


@configuracao.route("/", methods=['GET', 'POST'])
@login_required
def index():
    form = FormConfig()
    config = Config.query.get(1)
    if request.method == 'GET':
        form.orgao.data = config.orgao
        form.sigla_orgao.data = config.sigla_orgao
        form.sigla_sistema.data = config.sigla_sistema
        form.unidade_bloqueio.data = config.unidade_bloqueio
        form.validacao_processo.data = config.valida_processo

    elif request.method == 'POST' and form.validate_on_submit():
        config.orgao = form.orgao.data
        config.sigla_orgao = form.sigla_orgao.data
        config.sigla_sistema = form.sigla_sistema.data
        config.unidade_bloqueio = form.unidade_bloqueio.data
        config.token = form.token.data
        config.valida_processo = form.validacao_processo.data
        db.session.commit()
        flash('Configuração atualizada com sucesso!', 'alert-success')
        return redirect(url_for('configuracao.index'))

    return render_template("configuracao/index.html", form=form)
