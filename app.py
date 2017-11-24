from flask import Flask, g
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from config import Config
from flask_sqlalchemy import SQLAlchemy
# from werkzeug.contrib.fixers import ProxyFix
# import logging
# from logging.handlers import RotatingFileHandler


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager(app)
login_manager.login_view = "login"

@app.before_request
def _before_request():
    g.user = current_user

bcrypt = Bcrypt(app)


    # gunicorn stuff here
# app.wsgi_app = ProxyFix(app.wsgi_app)

# log handler
# file_handler = RotatingFileHandler('flask.log', maxBytes=1024 * 1024 * 100, backupCount=20)
# file_handler.setLevel(logging.DEBUG)
# formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# file_handler.setFormatter(formatter)
# app.logger.addHandler(file_handler)