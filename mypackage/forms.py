from wtforms import SelectField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=20)],
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=55)]
    )


class RegisterForm(FlaskForm):
    """User registration form."""
    email = StringField(
        "Email",
        validators=[InputRequired(), Email(), Length(max=50)]
    )

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=20)]
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=55)]
    )

    image_url = StringField('(Optional) Image URL')

class DeleteForm(FlaskForm):
    """Delete form -- this form is intentionally blank."""