from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.fields.html5 import DateField
from webapp.models import User, TwitterQuery
from datetime import datetime, timedelta


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username already exist.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email already exist.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class TwitterForm(FlaskForm):
    twitter_query = StringField('Query', validators=[DataRequired()], render_kw={"placeholder": "Query"})
    to_date = DateField('To Date', default=datetime.today(),)
    from_date = DateField('From Date', default=datetime.today() - timedelta(days=7))
    numbers_of_tweets = IntegerField('How Many Tweets', default=1000, validators=[DataRequired()])
    retweet = BooleanField('Include retweets') 
    source = SelectField(label='Source', choices=[('hashtag', '#hashtag'),('word','Word'),('user','User')])
    submit = SubmitField('Collect tweets')


class RaportForm(FlaskForm):
    positive = BooleanField('Positive')
    neutral = BooleanField('Neutral')
    negative = BooleanField('Negative')

    morning = BooleanField('Morning')
    midday = BooleanField('Midday')
    afternoon = BooleanField('Afternoon')
    evening = BooleanField('Evening')
    night = BooleanField('Night')

    submit = SubmitField('Generate Raport')
