from flask import Flask, g, session, request, url_for, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from config import config
from flask.ext.login import LoginManager
from flask_wtf.csrf import CsrfProtect
from flask.ext.bootstrap import Bootstrap
from flask.ext import restful

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "main.RegLogin"
login_manager.session_protection = "strong"

csrf = CsrfProtect()
bootstrap = Bootstrap()
api = restful.Api()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app( app )
    login_manager.init_app( app )
    csrf.init_app(app)
    bootstrap.init_app(app)
    api.init_app(app)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix="/admin")

    return app
