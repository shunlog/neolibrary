from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

class SearchForm(FlaskForm):
    search = StringField('Search')
