#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = os.environ['SECRET_KEY']

# list of OpenID
OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

# Path where SQLAlchemy-migrate stores data files
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_RECORD_QUERIES = True
WHOOSH_BASE = os.path.join(basedir, 'search.db')

# Disable Whoosh on Heroku
WHOOSH_ENABLED = os.environ.get('HEROKU') is None

# slow database query treshold (in seconds)
DATABASE_QUERY_TIMEOUT = 0.5

# Mail server settings local
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None

# Mail server settings for googlemail
# MAIL_SERVER = 'smtp.googlemail.com'
# MAIL_PORT = 465
# MAIL_USE_TLS = False
# MAIL_USE_SSL = True
# set environ vars
# $ export MAIL_USERNAME=username ...
# MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
# MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

# administrator list
ADMINS = ['you@example.com']

LANGUAGES = {
    'en': 'English',
    'es': 'Español',
    'de': 'Deutsch'
}

# microsoft translation service
MS_TRANSLATOR_CLIENT_ID = os.environ['MS_TRANSLATOR_CLIENT_ID']
MS_TRANSLATOR_CLIENT_SECRET = os.environ['MS_TRANSLATOR_CLIENT_SECRET']

# pagination
POSTS_PER_PAGE = 50
MAX_SEARCH_RESULTS = 50
