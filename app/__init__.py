from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

# creation of the flask object
app = Flask(__name__)
# read the config file
app.config.from_object('config')
# creating a db object that will be the database
db = SQLAlchemy(app)

from app import views, models
