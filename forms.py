from flask_wtf import Form
from wtforms import PasswordField, SubmitField, validators
from wtforms.fields.html5 import EmailField

class RegistrationForm(Form):
    email = EmailField('email', 
                        validators=[validators.DataRequired(), 
                                    validators.Email()])
    password = PasswordField('password',
                              validators=[validators.DataRequired(),
                              validators.Length(min=8, 
                                                message="Please choose a password of at least 8 characters")])
    password2 = PasswordField('password2', 
                               validators=[validators.DataRequired(),
                               validators.EqualTo('password', message="Passwords must match")])

    submit = SubmitField('submit', validators=[validators.DataRequired()])

class LoginForm(Form):
    email = EmailField('email',
                        validators=[validators.DataRequired(),
                                    validators.Email()])

    password = PasswordField('password',
                              validators=[validators.DataRequired(),])