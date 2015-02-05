#!/usr/bin/env python
"""
    The SQLAlchemy-migrate package comes with command line tools and APIs to
    create databases in a way that allows easy updates.

    This script invokes the migration API to create a db. It is completely
    generic. All the application specific pathnames are imported from the
    config file. For a new project just copy the script to the new app's
    directory and it will work right away.
"""

from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import db
import os.path
db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO,
                        api.version(SQLALCHEMY_MIGRATE_REPO))
