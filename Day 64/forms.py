"""
Day 64: Movie Forms with Flask-WTF
"""

from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class RateMovieForm(FlaskForm):
    rating = FloatField(
        "Your Rating Out of 10 (e.g. 8.5)",
        validators=[
            DataRequired(message="Rating is required."),
            NumberRange(min=0.0, max=10.0, message="Rating must be between 0.0 and 10.0")
        ]
    )
    review = StringField("Your Review", validators=[DataRequired(message="Please enter your personal review.")])
    submit = SubmitField("Update Movie Record")


class FindMovieForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired(message="Please enter a movie title to search.")])
    submit = SubmitField("Search Movie Database")
