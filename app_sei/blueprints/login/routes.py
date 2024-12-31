from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from app_sei.blueprints.login.forms import FormLogin
from app_sei.blueprints.login.functions.auth import auth
from functools import wraps

login = Blueprint('login', __name__, template_folder='templates')


def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if 'usuario' in session:
            return function(*args, **kwargs)
        else:
            flash('Faça login novamente para acessar essa página!', 'alert-danger')
            return redirect(url_for('login.index'))

    return wrapper


@login.route('/', methods=['GET', 'POST'])
def index():
    """
    This function handles the login page.
    It validates the form and calls the auth function if the form is valid.
    """
    form = FormLogin()
    if form.validate_on_submit() and 'botao_submit' in request.form:
        usuario = form.usuario.data
        senha = form.senha.data
        response_auth = auth(usuario, senha)
        session.clear()
        session['usuario'] = response_auth
        if response_auth.get('acesso'):
            flash(f'Login realizado com sucesso!', 'alert-success')
            return redirect(url_for('core.index'))
        else:
            flash(f'{response_auth.get("mensagem")}', 'alert-danger')
            return redirect(url_for('login.index'))

    return render_template('login/index.html', form=form)


@login.route('/logout')
@login_required
def logout():
    session.clear()
    flash('Log out realizado com sucesso', 'alert-success')
    return redirect(url_for('login.index'))
