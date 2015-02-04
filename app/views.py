from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Stephan'}
    posts = [
  {
    "author": {
      "nickname": "Corrine Pitts"
    },
    "body": "Tempor anim dolore reprehenderit sit nisi cupidatat exercitation."
  },
  {
    "author": {
      "nickname": "Evangeline Reeves"
    },
    "body": "Eu consectetur irure eiusmod culpa enim ipsum et dolore labore."
  },
  {
    "author": {
      "nickname": "Rosalie Rosa"
    },
    "body": "Irure anim voluptate duis anim amet."
  },
  {
    "author": {
      "nickname": "Abigail Lawrence"
    },
    "body": "Non ad deserunt aliquip elit irure duis officia do ea."
  },
  {
    "author": {
      "nickname": "Hopper Hopkins"
    },
    "body": "Aute et duis deserunt elit id voluptate sit irure magna incididunt est sit anim ullamco."
  }
]
    return render_template("index.html",
                           title='Pycodeshare',
                           user=user,
                           posts=posts)
