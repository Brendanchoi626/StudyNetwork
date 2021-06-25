# imports
import sqlite3
from flask import Flask, render_template, request, session, redirect, url_for, Blueprint, g, abort
import flask_sqlalchemy
from flask_sqlalchemy.model import Model
from config import Config
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date


def sqlite_conn(database, query, single=False):
    "connects to a database and returns data"
    conn = sqlite3.connect(database)
    cur = conn.cursor() 
    cur.execute(query) 
    results = cur.fetchone() if single else cur.fetchall() 
    conn.close() 
    return results 

#from main import db

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

import models
from forms import Sign_in, Sign_up

#routes#

@app.route('/')
def home():
    "The homepage route"
    post = models.Post.query.all()
    user_info = sqlite_conn('data.db', 'SELECT * FROM User WHERE id = (SELECT user_id FROM Post)', True)
    return render_template('home.html', post=post, user_info=user_info[1], title='home')


@app.route('/post', methods=['GET', 'POST'])
def post():
    "Route for post. Allows the player to make new posts."
    if g.logged_in_user == None:
        return redirect(url_for('user'))

    elif request.method == 'POST':
        post_info = models.Post(

            title = request.form.get('title'),
            discussion = request.form.get('discussion'),
            date = date.today().strftime("%d%m%Y"),
            likes = 0,
            user_id = session['logged_in_user']

        )      
        db.session.add(post_info)
        db.session.commit()

        posts = models.Post.query.filter_by(user_id = session['logged_in_user']).all()
        #aimpost = posts[-1][0]
        category = request.form.get('categories')
        #print(aimpost)
        print(category)

        

    return render_template('post.html')
        

@app.route('/noti')
def noti(id):
    
    return render_template('noti.html', title='noti')


@app.route('/profile')
def profile():
    "Profile route. If the user is signed in, it returns the profile page with user info. Else returns signup page"
    if g.logged_in_user:
        user_info = sqlite_conn('data.db', 'SELECT * FROM User WHERE id = {}'.format(session['logged_in_user']), True)
        post_info = models.Post.query.filter_by(user_id = session['logged_in_user']).all()
        #post_info = models.User.query.filter_by(id=session['logged_in_user']).first()
        #posts = sqlite_conn('data.db', 'SELECT * FROM Post WHERE id = (SELECT Post_id FROM PostUser WHERE User_id = {})'.format(session['logged_in_user']), True)
        return render_template('profile.html', id=user_info[0], username=user_info[1], email=user_info[2], post=post_info)

    return redirect(url_for('user'))


@app.route('/user', methods=['GET', 'POST'])
def user():
    "Sign in route. Checks if the user information is correct and redirects to profile page."
    usern = models.User.query.filter_by(username = request.form.get('username_or_email')).first()
    usere = models.User.query.filter_by(email = request.form.get('username_or_email')).first()
    password = request.form.get('password')
    if request.method == 'POST':
        session.pop('logged_in_user', None)
        #Check if the username/password is matching
        if usern == None and usere == None:
            return render_template('user.html', error = 'please check your username/password again')
        else:
            try:
                passwith = check_password_hash(usern.password, password)                             
            except:
                passwith = check_password_hash(usere.password, password)
            finally:
                if not passwith:
                    return render_template('user.html', error = 'please check your username/password again') 
        #redirects profile if it matches
        if usere == None:
            session['logged_in_user'] = usern.id
            return redirect(url_for('profile'))
        else:
            session['logged_in_user'] = usere.id
            return redirect(url_for('profile'))

    return render_template('user.html')


@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    "Sign up route. Allows you to create a new account with the input information if possible."
    form = Sign_up()
    if request.method == "GET": #If browser asked to see the page
        return render_template('signup.html', form=form, title='sign_up')
    
    else:
        if form.validate_on_submit():
            if models.User.query.filter_by(username = request.form.get('username')).first() != None:
                return render_template('signup.html', form=form, error = 'username already in use')

            if models.User.query.filter_by(email = request.form.get('email')).first() != None:
                return render_template('signup.html', form=form, error = 'email already in use')

            if len(request.form.get('password')) < 8:
                return render_template('signup.html', form=form, error='password must be atleast 8 letters')

            if request.form.get('password') != request.form.get('re-password'):
                return render_template('signup.html', form=form, error = 'your passwords do not match. Please try again')

            else:# if possible, create an account. 
                user_info = models.User(
                    username = form.username.data,
                    email = form.email.data,
                    password = generate_password_hash(form.password.data, method='sha256')
                )
                db.session.add(user_info)
                db.session.commit()
                return redirect(url_for('user'))
        
        else:
            return render_template('signup.html', form=form, title='sign_up')

    

    


    if request.method == 'POST':#Checks if the users can create a new account with input information

        if models.User.query.filter_by(username = request.form.get('username')).first() != None:
            return render_template('signup.html', error = 'username already in use')

        if models.User.query.filter_by(email = request.form.get('email')).first() != None:
            return render_template('signup.html', error = 'email already in use')

        if len(request.form.get('password')) < 8:
            return render_template('signup.html', error='password must be atleast 8 letters')

        if request.form.get('password') != request.form.get('re-password'):
            return render_template('signup.html', error = 'your passwords do not match. Please try again')

        

    return render_template('signup.html')


@app.route('/logout')
def logout():
    "Route for logout."
    session.pop('logged_in_user', None)

    return redirect(url_for('user'))


@app.before_request
def before_request():
    "Called before the request, checks if anybody is logged in."
    g.logged_in_user = None
    if 'logged_in_user' in session:
        g.logged_in_user = session['logged_in_user']


if __name__ == "__main__":
    app.run(debug=True)