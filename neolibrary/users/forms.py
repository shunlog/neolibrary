from flask_login import login_user, current_user, logout_user, login_required
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from neolibrary import app, graph 
from neolibrary.models import User 

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[
                                         DataRequired(),
                                         EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User()
        ls = list( User.match(graph).where("_.username =~ '{}'"
                                           .format(username.data)))
        print(username,':',ls)
        if len(ls) != 0:
            raise ValidationError('This username is already taken')

    def validate_email(self, email):
        user = User()
        ls = list( User.match(graph).where("_.email =~ '{}'".format(email.data)))
        if len(ls) != 0:
            raise ValidationError('Account with such email already exists')



class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    
class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture',
                        validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        print("validating username:",username.data)
        if username.data != current_user.username:
            user = User.match(graph).where(username=username.data).first()
            if user:
                raise ValidationError('That username is taken.\
                Please choose a different one.')

    def validate_email(self, email):
        print("validating email:",email.data)
        if email.data != current_user.email:
            user = User.match(graph).where(email=email.data).first()
            if user:
                raise ValidationError('That email is taken.\
                Please choose a different one.')
