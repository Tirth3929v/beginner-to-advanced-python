"""
Day 67: Create & Edit Blog Post WTForms
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, URL


class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired(message="Title is required.")])
    subtitle = StringField("Subtitle", validators=[DataRequired(message="Subtitle is required.")])
    author = StringField("Your Name (Author)", validators=[DataRequired(message="Author name is required.")])
    img_url = StringField("Header Background Image URL", validators=[
        DataRequired(message="Header image URL is required."),
        URL(message="Must be a valid image URL (e.g. https://images.unsplash.com/...)")
    ])
    body = TextAreaField("Blog Content (HTML / Markdown supported)", validators=[DataRequired(message="Body content is required.")])
    submit = SubmitField("Publish Article")
