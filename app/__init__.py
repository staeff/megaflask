import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir

# creation of the flask object
app = Flask(__name__)
# read the config file
app.config.from_object('config')
# creating a db object that will be the database
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
# configure the login page/view
lm.login_view = 'login'
# Flask-OpenID needs a path where files can be stored
oid = OpenID(app, os.path.join(basedir, 'tmp'))

from app import views, models
