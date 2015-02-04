from flask import Flask

# creation of the flask object
app = Flask(__name__)
# read the config file
app.config.from_object('config')

from app import views
