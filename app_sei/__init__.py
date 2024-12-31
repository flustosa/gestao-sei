# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
# from flask_login import LoginManager
# import os
# import sqlalchemy
#
# app = Flask("__name__", template_folder='./app_sei/templates/', static_folder='./app_sei/static', static_url_path='/')
# app.config['SECRET_KEY'] = "50f68db4cdfd3d5b6fad331e468f71ae"
#
# if os.getenv('DATABASE_URL'):
#     app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
# else:
#     app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///site_flask.db'
#
# database = SQLAlchemy(app)
# bcrypt = Bcrypt(app)
#
# from app_sei import routes


