"""
Day 69: WTForms Definitions for Blog, Authentication & Comments
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, URL, Email, Length


class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired(message="Title is required.")])
    subtitle = StringField("Subtitle", validators=[DataRequired(message="Subtitle is required.")])
    img_url = StringField("Header Background Image URL", validators=[
        DataRequired(message="Image URL is required."),
        URL(message="Must be a valid URL (e.g. https://images.unsplash.com/...)")
    ])
    body = TextAreaField("Blog Content (HTML supported)", validators=[DataRequired(message="Body content is required.")])
    submit = SubmitField("Publish Article")


class RegisterForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired(message="Name is required.")])
    email = StringField("Email Address", validators=[
        DataRequired(message="Email is required."),
        Email(message="Please provide a valid email.")
    ])
    password = PasswordField("Password", validators=[
        DataRequired(message="Password is required."),
        Length(min=8, message="Password must be at least 8 characters.")
    ])
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    email = StringField("Email Address", validators=[
        DataRequired(message="Email is required."),
        Email(message="Please provide a valid email.")
    ])
    password = PasswordField("Password", validators=[DataRequired(message="Password is required.")])
    submit = SubmitField("Log In")


class CommentForm(FlaskForm):
    comment_text = TextAreaField("Leave a Comment", validators=[DataRequired(message="Comment cannot be empty.")])
    submit = SubmitField("Submit Comment")
