from flask import Flask, helpers
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os


root_path = helpers.get_root_path('app')
load_dotenv(os.path.join(root_path, '.env'))
secret = os.getenv('SECRET_KEY')

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, template_folder='./templates', static_folder='./static')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./webapp.db'
    app.config['SECRET_KEY'] = secret

    with app.app_context():
        db.init_app(app)


    # import and register all blueprints
    from app_sei.blueprints.configuracao.routes import configuracao
    from app_sei.blueprints.core.routes import core
    from app_sei.blueprints.login.routes import login
    from app_sei.blueprints.bloqueio.routes import bloqueio

    app.register_blueprint(login, url_prefix='/')
    app.register_blueprint(configuracao, url_prefix='/configuracao')
    app.register_blueprint(core, url_prefix='/core')
    app.register_blueprint(bloqueio, url_prefix='/bloqueio')

    migrate = Migrate(app, db)

    return app
