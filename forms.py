from flask.app import Flask
from flask_wtf import Form
from flask_wtf.form import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import widgets, SelectMultipleField, SubmitField, PasswordField
from wtforms.fields.simple import HiddenField, TextField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, Optional, ValidationError
from wtforms.widgets.core import TextArea
import models
from flask import session


class MultiCheckBoxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class Post(FlaskForm):
    title = TextField('title', validators=[DataRequired()])
    discussion = TextAreaField('discussion', validators=[DataRequired()]) 
    categories = [{'id':"1", 'topic':"Maths"}, {'id':"2", 'topic':"Physics"}, {'id':"3", 'topic':"Biology"}, {'id':"4", 'topic':"Chemistry"}, {'id':"5", 'topic':"English"}, {'id':"6", 'topic':"Economics/Business"}, {'id':"7", 'topic':"Programming"}, {'id':"8", 'topic':"other"}]
    files = [(x['id'], x['topic']) for x in categories]
    category = MultiCheckBoxField('Label', choices=files)


class Sign_up(FlaskForm):
    username = TextField('username', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    re_password = PasswordField('re-password', validators=[DataRequired()])


class Sign_in(FlaskForm):
    username_or_email = TextField('username_or_email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class Comment(FlaskForm):
    comment = TextAreaField('Write your comment or reply here', validators=[DataRequired()])