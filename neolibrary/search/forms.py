from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError


class SearchForm(FlaskForm):
    choices = [('Book', 'Book'),
               ('Author', 'Author'),
               ('Tag', 'Tag')]
    select = SelectField('Search:', choices=choices)
    search = StringField('search', id='form-search')
