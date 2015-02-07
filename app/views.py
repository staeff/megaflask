import json
from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm



posts

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Stephan'}
    with open('posts.json', 'r') as f:
        posts = json.load(f)

    return render_template("index.html",
                           title='Pycodeshare',
                           user=user,
                           posts=posts)


# accept GET and POST requests. Without this only GET requests are accepted
@app.route('/login', methods=['GET', 'POST'])
def login():
    ''' View function that renders the template. '''

    # Instantiate an object from LoginForm class to send it later to the
    # template
    form = LoginForm()
    # True if all validations successful
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])
