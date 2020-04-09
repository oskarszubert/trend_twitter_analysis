from flask import render_template, url_for, flash, redirect, request
from webapp import app, db, bcrypt
from webapp.forms import RegistrationForm, LoginForm, TwitterForm, RaportForm
from webapp.models import User, TwitterQuery
from flask_login import login_user, current_user, logout_user
from webapp.OnlineMenu import twitter_flask, generate_raport
import os

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        twitter_queries = TwitterQuery.query.filter_by(user=current_user).order_by(TwitterQuery.id.desc())

    form = TwitterForm()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            query = TwitterQuery(   twitter_query=form.twitter_query.data,
                                    to_date=form.to_date.data,
                                    from_date=form.from_date.data,
                                    retweet=form.retweet.data,
                                    user=current_user
                                )

            df = twitter_flask( query=form.twitter_query.data,
                                source=form.source.data,
                                retweet=form.retweet.data,
                                numbers_of_tweets=int(form.numbers_of_tweets.data),
                                to_date=str(form.to_date.data),
                                from_date=str(form.from_date.data)
                              )
            
            if df[1]:
                query.filename = df[0]
                query.numbers_of_tweets = df[1]

                db.session.add(query)
                db.session.commit()
                flash('Tweets collected!', 'success')
            else:
                flash('No tweets found!', 'danger')
            return redirect('/index')
        return render_template('index.html', form=form, twitter_queries=twitter_queries)
    else:
        return redirect(url_for('login'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        else:
            flash('Invalid Email or Password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/raport/<int:query_id>", methods=['GET', 'POST'])
def raport(query_id):
    twitter_query = TwitterQuery.query.get_or_404(query_id)
    form = RaportForm()
    data_from_raport = generate_raport(form=form, filename=twitter_query.filename)
    return render_template('raport.html',
                           form=form,
                           twitter_query=twitter_query,
                           data_from_raport=data_from_raport,
                           title='Raport: '+twitter_query.twitter_query)


@app.route("/raport/<int:query_id>/delete", methods=['POST'])
def delete_query(query_id):
    twitter_query = TwitterQuery.query.get_or_404(query_id)
    if twitter_query.user != current_user:
        abort(403)
    os.remove('collected_data/tagged/'+twitter_query.filename+'.xlsx')
    db.session.delete(twitter_query)
    db.session.commit()
    flash('Deleted twitter data!', 'info')
    return redirect(url_for('index'))
