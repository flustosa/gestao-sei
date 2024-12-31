from flask import render_template, Blueprint, session
from app_sei.blueprints.configuracao.models import Config
from app_sei.blueprints.login.routes import login_required
from app_sei.app import db

core = Blueprint('core', __name__, template_folder='templates')


@core.route('/')
@login_required
def index():
    # Routes da página principal após o login. O objetivo aqui é carregar os parâmetros do Webservice armazendados
    # no Sqlite e, caso não existam, passar parâmetros genéricos para evitar uma Exception ou ter que tratar erros
    # em todas as páginas que possuem operações.

    user_session = session['usuario']
    try:
        config = Config.query.get(1)
        config_sistema = {
            "sigla_orgao": config.sigla_orgao,
            "orgao": config.orgao,
            "sigla_sistema": config.sigla_sistema,
            "unidade_bloqueio": config.unidade_bloqueio,
            "token": config.token,
        }
    except:  # Essa Exception é apenas para inicialização da aplicação, pode ser resolvido posteriormente
        # com a inclusão de variáveis de ambiente genéricas para a inicializar sem bug.
        config_sistema = Config(
            sigla_orgao="ORGAO",
            orgao="NOME ORGAO",
            sigla_sistema="SISTEMA",
            unidade_bloqueio="UNIDADE",
            token="TOKEN",
            valida_processo=True
        )
        db.session.add(config_sistema)
        db.session.commit()
    print(f"Configuracao do sistema: {config_sistema}")
    print(f"Sessão do usuário: {user_session}")
    return render_template('core/index.html', user_session=user_session)

