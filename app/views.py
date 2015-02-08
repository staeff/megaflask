import json
from flask import render_template, flash, redirect, session
#
from flask import url_for
# The g global is setup by Flask to store and share data
# during the life of a request.
from flask import request, g
from flask.ext.login import login_user, logout_user, current_user, \
    login_required
from app import app, db, lm, oid
from .forms import LoginForm
from .models import User

# load_user is registered with Flask-Login through this decorator
@lm.user_loader
def load_user(id):
    """ load a user from the database. id is stored as unicode and needs to
    be converted to an int for the query."""
    return User.query.get(int(id))


@app.before_request
def before_request():
    """ Setup g.user variable. The 'current_user' global is set by Flask-Login.
    For better access a copy is saved to the g object.
    This allows all all requests to access the logged in user,
    even inside templates. """
    g.user = current_user


@app.route('/')
@app.route('/index')
# page only visible for logged in users
@login_required
def index():
    user = g.user
    with open('posts.json', 'r') as f:
        posts = json.load(f)

    return render_template("index.html",
                           title='Pycodeshare',
                           user=user,
                           posts=posts)


# accept GET and POST requests. Without this only GET requests are accepted
@app.route('/login', methods=['GET', 'POST'])
# tells Flask-OpenID that this is our login view function.
@oid.loginhandler
def login():
    ''' View function that renders the template. '''
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    # Instantiate an object from LoginForm class to send it later to the
    # template
    form = LoginForm()
    # True if all validations successful
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        # trigger the user authentication through Flask-OpenID.
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])

@oid.after_login
def after_login(resp):
    """ resp contains information returned by the OpenID provider. """
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        # some OpenID providers don't have the nickname.
        if nickname is None or nickname == '':
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
