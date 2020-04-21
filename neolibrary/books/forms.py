from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])

    authors = StringField('Author', validators=[])
    hidden_authors = HiddenField("hidden-authors", id="hidden_authors_id")

    tags = StringField('Tags', validators=[])
    hidden_tags = HiddenField("hidden-tags", id="hidden_tags_id")

    picture = FileField('Update Profile Picture',
                        validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    link = StringField('Or paste link to image')
    submit = SubmitField('Post')
