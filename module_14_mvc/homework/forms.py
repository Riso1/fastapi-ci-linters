from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired

class BookForm(FlaskForm):
    book_title = StringField("Book title", validators=[InputRequired()])
    author_name = StringField("Author full name", validators=[InputRequired()])