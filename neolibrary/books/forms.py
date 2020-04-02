from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    authors = StringField('Author', validators=[DataRequired()])
    tags = StringField('Tags', validators=[DataRequired()])
    picture = FileField('Update Profile Picture',
                        validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    link = StringField('Or paste link to image')
    submit = SubmitField('Post')
