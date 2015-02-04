from flask.ext.wtf import Form
from wtforms import StringField, BooleanField

# DataRequired is a validator, a function that
# can be attached to a field to perform validation
# on the data submitted by the user.
from wtforms.validators import DataRequired


class LoginForm(Form):
    # Fields of the form are defined as class variables.

    # DataRequired checks that the field is not empty
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
