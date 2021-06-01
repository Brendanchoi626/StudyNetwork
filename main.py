# imports
from flask import Flask, render_template, request, session, redirect, url_for, Blueprint, flash
from config import Config
from flask_sqlalchemy import SQLAlchemy

#from main import db

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

import models

#routes#
@app.route('/')
def home():
    post = models.Post.query.all()
    return render_template('home.html', post=post, title='home')


@app.route('/post')
def post():
    return render_template('post.html', title='post')

@app.route('/noti/<int:id>')
def noti(id):

    return render_template('noti.html', title='noti')


@app.route('/profile/<int:id>')
def profile(id):
    return render_template('profile.html', title='profile')


@app.route('/user', methods=['GET', 'POST'])
def user():
    usern = models.User.query.filter_by(username = request.form.get('username_or_email')).first()
    email = models.User.query.filter_by(email = request.form.get('username_or_email')).first()
    password = models.User.query.filter_by(password = request.form.get('password')).first()
    if request.method == 'POST':
        if usern == None:
            if email == None:
                return render_template('user.html', error = 'please check your username/password again')
        elif password == None:
            return render_template('user.html', erorr = 'please check your username/password again')
        else:
            if usern != None:
                return render_template('profile.html', id = usern.id)
            elif email != None:
                return render_template('profile.html', id = email.id)
    return render_template('user.html')


@app.route('/signup', methods = ['GET', 'POST'])
def signup():#Signup route 
    if request.method == 'POST':#Checks if the users can create a new account with input information
        if models.User.query.filter_by(username = request.form.get('username')).first() != None:
            return render_template('signup.html', error = 'username already in use')
        if models.User.query.filter_by(email = request.form.get('email')).first() != None:
            return render_template('signup.html', error = 'email already in use')
        if len(request.form.get('password')) < 8:
            return render_template('signup.html', error='password must be atleast 8 letters')
        if request.form.get('password') != request.form.get('re-password'):
            return render_template('signup.html', error = 'your passwords do not match. Please try again')
        else:# if possible, create an account. 
            user_info = models.User(

                username = request.form.get('username'),
                email = request.form.get('email'),
                password = request.form.get('password')

            )
            db.session.add(user_info)
            db.session.commit()
    return render_template('signup.html')


if __name__ == "__main__":
    app.run(debug=True)