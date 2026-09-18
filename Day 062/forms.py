"""
Day 62: Cafe Submission WTForms Definition
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL


class CafeForm(FlaskForm):
    cafe = StringField("Cafe Name", validators=[DataRequired(message="Please provide a cafe name.")])
    location = StringField("Cafe Location on Google Maps (URL)", validators=[
        DataRequired(message="Location URL is required."),
        URL(message="Must be a valid URL (e.g. https://maps.google.com/...)")
    ])
    open_time = StringField("Opening Time (e.g. 8:00 AM)", validators=[DataRequired()])
    closing_time = StringField("Closing Time (e.g. 10:00 PM)", validators=[DataRequired()])
    
    coffee_rating = SelectField(
        "Coffee Quality Rating",
        choices=["☕", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"],
        validators=[DataRequired()]
    )
    wifi_rating = SelectField(
        "WiFi Speed & Reliability",
        choices=["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"],
        validators=[DataRequired()]
    )
    power_rating = SelectField(
        "Power Socket Availability",
        choices=["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"],
        validators=[DataRequired()]
    )
    submit = SubmitField("Submit Cafe Listing")
