from flask_wtf import Form
from flask_wtf.form import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import widgets, SelectMultipleField, SubmitField
from wtforms.fields.simple import TextField, TextAreaField
from wtforms.validators import DataRequired, Optional, ValidationError
import models


class MultiCheckBoxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class Sign_up(FlaskForm):

    username = TextField('username', validators=[DataRequired()])
    email = TextField('email', validators=[DataRequired()])
    password = TextField('password', validators=[DataRequired()])
    re_password = TextField('re-password', validators=[DataRequired()])


class Sign_in(FlaskForm):

    username_or_email = TextField('username_or_email', validators=[DataRequired()])
    password = TextField('password', validators=[DataRequired()])

    