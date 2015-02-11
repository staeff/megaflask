import os
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, \
    MAIL_PASSWORD

# creation of the flask object
app = Flask(__name__)
# read the config file, but which values does it actually read?
app.config.from_object('config')
# creating a db object that will be the database
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
# configure the login page/view
lm.login_view = 'login'
# Flask-OpenID needs a path where files can be stored
oid = OpenID(app, os.path.join(basedir, 'tmp'))

# error-emails are only enabled, when we are not in debugging mode
if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT),
                               'no-reply' + MAIL_SERVER, ADMINS,
                               'microblog failure', credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

# logfiles are only enabled, when we are not in debugging mode
if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/microblog.log', 'a',
                                        1 * 1024 * 1024, 10)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('microblog startup')

# debug toolbar
# app.debug = True
toolbar = DebugToolbarExtension(app)

from app import views, models
