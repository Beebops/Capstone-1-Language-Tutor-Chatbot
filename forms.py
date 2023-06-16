from wtforms import StringField, PasswordField, ValidationError, SelectField
from wtforms.validators import EqualTo
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, Email
from models import User
import email_validator
from flask_login import current_user


class login_form(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired()], render_kw={"class": "form-control"}
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=8, max=72)],
        render_kw={"class": "form-control"},
    )


class registration_form(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Email(), Length(1, 64)])
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=8, max=72)]
    )
    password_copy = PasswordField(
        "Re-enter Password",
        validators=[
            InputRequired(),
            Length(min=8, max=72),
            EqualTo("password", message="Passwords must match!"),
        ],
    )

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Email already registered!")

    def validate_usrname(self, usrname):
        if User.query.filter_by(username=usrname.data).first():
            raise ValidationError("Username already taken!")


class new_chat_form(FlaskForm):
    language_choices = [
        ("spanish", "Spanish"),
        ("french", "French"),
        ("german", "German"),
        ("italian", "Italian"),
    ]
    difficulty_choices = [("b1", "B1"), ("b2", "B2"), ("c1", "C1"), ("c2", "C2")]
    language = SelectField(
        "Language", choices=language_choices, validators=[InputRequired()]
    )
    language_level = SelectField(
        "Difficulty Level", choices=difficulty_choices, validators=[InputRequired()]
    )
