from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField 
from wtforms.validators import DataRequired

class TagForm(FlaskForm):
    name = StringField('Name', id='form-tags', validators=[DataRequired()])
    submit = SubmitField('Post')
