from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField

# DataRequired is a validator, a function that
# can be attached to a field to perform validation
# on the data submitted by the user.
from wtforms.validators import DataRequired, Length
from .models import User

class LoginForm(Form):
    # Fields of the form are defined as class variables.

    # DataRequired checks that the field is not empty
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class EditForm(Form):
    nickname = StringField('nickname', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])

    def __init__(self, original_nickname, *args, **kwargs):
        """ The form constructor takes the original_nickname.  """
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname

    def validate(self):
        if not Form.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        user = User.query.filter_by(nickname=self.nickname.data).first()
        if user is not None:
            self.nickname.errors.append('This nickname is already in user. '
                                        'Please choose another one.')
            return False
        return True

class PostForm(Form):
    post = StringField('post', validators=[DataRequired()])

class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])
