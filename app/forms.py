from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField

# DataRequired is a validator, a function that
# can be attached to a field to perform validation
# on the data submitted by the user.
from wtforms.validators import DataRequired, Length


class LoginForm(Form):
    # Fields of the form are defined as class variables.

    # DataRequired checks that the field is not empty
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class EditForm(Form):
    nickname = StringField('nickname', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])
