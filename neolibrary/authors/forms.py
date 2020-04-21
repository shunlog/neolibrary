from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField 
from wtforms.validators import DataRequired

class AuthorForm(FlaskForm):
    name = StringField('Name', id='form-authors', validators=[DataRequired()])
    submit = SubmitField('Post')
