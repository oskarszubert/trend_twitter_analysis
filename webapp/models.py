from datetime import datetime
from webapp import db, login_manager
from flask_login import UserMixin
from datetime import datetime, timedelta

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    queris = db.relationship('TwitterQuery', backref='user', lazy=True)


class TwitterQuery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    twitter_query = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.today())
    to_date = db.Column(db.DateTime, nullable=False, default=datetime.today())
    from_date = db.Column(db.DateTime, nullable=False, default=datetime.today() - timedelta(days=7) )
    numbers_of_tweets = db.Column(db.Integer, nullable=False, default=200)
    retweet = db.Column(db.Boolean, default=False, nullable=False)
    filename =  db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
