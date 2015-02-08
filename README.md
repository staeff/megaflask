microblog
=========

A decently featured microblogging web application written in Python and Flask that I'm developing in my Flask Mega-Tutorial series that begins [here](http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).

Installation
------------

The tutorial referenced above explains how to setup a virtual environment with all the required modules.

The sqlite database must also be created before the application can run, and the `db_create.py` script takes care of that. See the [Database tutorial](http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database) for the details.

Running
-------

To run the application in the development web server just execute `run.py` with the Python interpreter from the flask virtual environment.

## Notes

**Database migrations**


* the db_downgrade.py script goes back one revision at a time
* the upgrade.py script goes directly to the latest revision.

Alembic as an alternative to SQLAlchemy-migrate.
https://alembic.readthedocs.org It is from the author of SQLAlchemy.

It would be great if you could update the tutorial to use (flask-)alembic
rather than the more or less abandoned sqlalchemy-migrate.
