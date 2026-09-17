"""
Day 61: WTForms Form Definitions
Defines type-safe, validated web forms with built-in CSRF token protection.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    """Secure login form enforcing email formatting and password length requirements."""
    email = StringField(
        label="Email Address",
        validators=[
            DataRequired(message="Email address is required."),
            Email(message="Please provide a valid email address (e.g. user@domain.com).")
        ]
    )
    password = PasswordField(
        label="Password",
        validators=[
            DataRequired(message="Password is required."),
            Length(min=8, message="Password must be at least 8 characters long.")
        ]
    )
    submit = SubmitField(label="Log In")
