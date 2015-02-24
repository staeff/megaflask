import json
from flask import render_template, flash, redirect, session
#
from flask import url_for
# The g global is setup by Flask to store and share data
# during the life of a request.
from flask import request, g
from flask.ext.login import login_user, logout_user, current_user, \
    login_required
from flask.ext.babel import gettext
from datetime import datetime
from app import app, db, lm, oid, babel
from .forms import LoginForm, EditForm, PostForm, SearchForm
from .models import User, Post
from .emails import follower_notification
from config import POSTS_PER_PAGE, MAX_SEARCH_RESULTS
from config import LANGUAGES

# load_user is registered with Flask-Login through this decorator
@lm.user_loader
def load_user(id):
    """ load a user from the database. id is stored as unicode and needs to
    be converted to an int for the query."""
    return User.query.get(int(id))

@babel.localeselector
def get_locale():
    """ Read the Accept-Languages header sent by the browser in the HTTP request
    and find the best matching language from the supported languages list.
    The best_match method does all the work. Where is it coming from?
    @babel.localeselector? How do I find this out?"""
    # return request.accept_languages.best_match(LANGUAGES.keys())

    # Forcing languages for debugging: de, es
    return 'de'

@app.before_request
def before_request():
    """ Setup g.user variable. The 'current_user' global is set by Flask-Login.
    For better access a copy is saved to the g object.
    This allows all all requests to access the logged in user,
    even inside templates. """
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
        # make SearchForm available to all templates
        g.search_form = SearchForm()
    g.locale = get_locale()

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@app.route('/' , methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
# page only visible for logged in users
@login_required
def index(page=1):
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, timestamp=datetime.utcnow(),
                author=g.user)
        db.session.add(post)
        db.session.commit()
        flash(gettext('Your post is now live!'))
        # force the browser to issue another request after the form submission
        # to avoid accidental resubmission of posts.
        return redirect(url_for('index'))
    # followed_posts() returns sqlalchemy object
    # The paginate method can be called on any query object
    posts = g.user.followed_posts().paginate(page, POSTS_PER_PAGE, False)
    return render_template("index.html",
                           title='Pycodeshare',
                           user=user,
                           form=form,
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
        flash(gettext('Invalid login. Please try again.'))
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        # some OpenID providers don't have the nickname.
        if nickname is None or nickname == '':
            nickname = resp.email.split('@')[0]
        nickname = User.make_valid_nickname(nickname)
        nickname = User.make_unique_nickname(nickname)
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
        # make the user (implicitely) follow him/herself
        # easily include the posts in the followed posts query -> tutorial pt. 8
        db.session.add(user.follow(user))
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

# <nickname> turns to be an argument to the 'user' function
@app.route('/user/<nickname>')
@app.route('/user/<nickname>/<int:page>')
@login_required
def user(nickname, page=1):
    user = User.query.filter_by(nickname=nickname).first()
    follower = user.followers.all()
    if user is None:
        flash(gettext('User {0} not found.'.format(nickname)))
        return redirect(url_for('index'))
    posts = user.posts.paginate(page, POSTS_PER_PAGE, False)
    return render_template('user.html',
                            user=user,
                            posts=posts,
                            follower=follower)

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    # pass the constructor argument
    form = EditForm(g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash(gettext('Your changes have been saved.'))
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form=form)

@app.route('/follow/<nickname>')
def follow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash(gettext('User {0} not found.'.format(nickname)))
        return redirect(url_for('index'))
    if user == g.user:
        flash(gettext('You can\'t follow yourself!'))
        return redirect(url_for('user', nickname=nickname))
    u = g.user.follow(user)
    if u is None:
        flash(gettext('Can not follow {0}.'.format(nickname)))
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash(gettext('You are now following {0}!'.format(nickname)))
    follower_notification(user, g.user)
    return redirect(url_for('user', nickname=nickname))

@app.route('/unfollow/<nickname>')
def unfollow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash(gettext('User {0} not found.'.format()))
        return redirect(url_for('index'))
    if user == g.user:
        flash(gettext('You can\'t unfollow yourself!'))
        return redirect(url_for('user', nickname=nickname))
    u = g.user.unfollow(user)
    if u is None:
        flash(gettext('Can not unfollow {0}.'.format(nickname)))
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash(gettext('You have stopped following {0}.'.format(nickname)))
    return redirect(url_for('user', nickname=nickname))

@app.route('/search', methods=['POST'])
@login_required
def search():
    """ This function collects the search query from the form and
    then redirects to search_results with this query as an argument.
    The search work isn't done directly here to avoid resubmission of
    the form through usage of the refresh button."""
    if not g.search_form.validate_on_submit():
        return redirect(url_for('index'))
    return redirect(url_for('search_results', query=g.search_form.search.data))

@app.route('/search_results/<query>')
@login_required
def search_results(query):
    """ """
    results = Post.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
    return render_template('search_results.html',
                            query=query,
                            results=results)
