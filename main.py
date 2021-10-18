# imports
import sqlite3
from flask import Flask, render_template, request, session, redirect, url_for, Blueprint, g, abort
import flask_sqlalchemy
from flask_sqlalchemy import model
from flask_sqlalchemy.model import Model
from sqlalchemy.sql.elements import Null
from wtforms import form
from config import Config
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from sqlalchemy import desc

#SQL query executer
def sqlite_conn(database, query, single=False):
    "connects to a database and returns data"
    conn = sqlite3.connect(database)
    cur = conn.cursor() 
    cur.execute(query) 
    results = cur.fetchone() if single else cur.fetchall() 
    conn.close() 
    return results 


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


#imports from the project
import models
from forms import Sign_in, Sign_up, Post, Comment


#routes#
@app.route('/', methods=['GET', 'POST'])
def home():
    "The homepage route"
    # gets all the posts in the database
    post = models.Post.query.order_by(desc(models.Post.id)).all()
    number_of_items = 0
    for p in post:
        number_of_items += 1
    return render_template('home.html', posts=post, title='home', n=int(number_of_items))


@app.route('/comment/<int:id>', methods=['GET', 'POST'])
def comment(id):
    "Route for comment"
    form = Comment()

    post_info = db.session.query(models.Post).filter_by(id = id).first_or_404()
    user_info = db.session.query(models.User).filter_by(id = session['logged_in_user']).first()
    comments = db.session.query(models.Comment).filter_by(Post_id = id).all()
    # when no one is logged in, tells the user to sign up
    if g.logged_in_user == None:
        return redirect(url_for('signin'))

    elif request.method == 'GET':# display all the comments in the post
        if comments == Null:
            return render_template('comment.html', form=form, post_info=post_info)
        else:
            return render_template('comment.html', form=form, comments=comments, post_info=post_info)

    else: #when someone trys to make a comment, make a comment and notify the owner of the post
        if form.validate_on_submit():
            comment_info = models.Comment()
            comment_info.Post_id = id
            comment_info.User_id = session['logged_in_user']
            comment_info.comment = form.comment.data
            db.session.add(comment_info)

            post_info.comments += 1
            if user_info.id != post_info.user_id:
                notification_info = models.Notification()
                notification_info.user_id = post_info.user_id
                notification_info.sender = user_info.username
                notification_info.content = form.comment.data
                notification_info.post_id = id

                db.session.add(notification_info)
            db.session.commit()
        
            return redirect(url_for('comment',id=id))


@app.route('/post', methods=['GET', 'POST'])
def post():
    "Route for post. Allows the player to make new posts."
    form = Post()
    # when no one is logged in, tells the user to sign up
    if g.logged_in_user == None:
        return redirect(url_for('signin'))

    # when user tries to make a post, lets the user to do so haha..     
    elif request.method == 'GET':
        return render_template('post.html', form=form, title='post')

    # when user triggers the submit button
    else:
        if form.validate_on_submit():
            post_info = models.Post()
            post_info.title = form.title.data
            post_info.discussion = form.discussion.data
            post_info.date = date.today().strftime("%d%m%Y")
            post_info.comments = 0
            post_info.user_id = session['logged_in_user']            
            print(post_info.id)
            post_info = db.session.merge(post_info)
            for catego in form.category.data: 
                category = db.session.query(models.Category).filter_by(id = catego).first()
                post_info.categories_post.append(category)

            db.session.add(post_info)
            db.session.commit()
            return redirect(url_for('home'))
         
    return render_template('post.html', form=form, title='post')
        

@app.route('/notification', methods=['GET', 'POST'])
def notification():
    "Notification route. Displays all notifications that belong to the logged in user."
    # when no one is logged in, tells the user to sign up
    if g.logged_in_user == None:
        return redirect(url_for('signin'))
    else: 
        #Show all the notification to the user 
        Noti = models.Notification.query.filter_by(user_id = session['logged_in_user']).all()
        return render_template('noti.html', noti=Noti, title='noti')


@app.route('/mark_read/<int:id>/<int:pid>')
def mark_read(id, pid):
    "A route that deletes the notifications which are read"
    noti_to_delete = models.Notification.query.filter_by(id = id).first_or_404()
    noti_to_delete = db.session.merge(noti_to_delete)
    db.session.delete(noti_to_delete)
    db.session.commit()
    return redirect(url_for('comment', id=pid))


@app.route('/profile/<int:id>')
def profile(id):
    "Profile route. If the user is signed in, it returns the profile page with user info. Else returns signup page"
    #Shows the basic information of a user with a certain id. 
    user_info = models.User.query.filter_by(id = id).first_or_404()
    post_info = models.Post.query.filter_by(user_id = id).all()
    if g.logged_in_user:
        logged_in_user_info = models.User.query.filter_by(id = session["logged_in_user"]).first_or_404()
        return render_template('profile.html', user=user_info, post=post_info, loginuser=logged_in_user_info)
    else:
        return render_template('profile.html', user=user_info, post=post_info)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    "Sign in route. Checks if the user information is correct and redirects to profile page."    
    form = Sign_in()

    usern = models.User.query.filter_by(username = request.form.get('username_or_email')).first()
    usere = models.User.query.filter_by(email = request.form.get('username_or_email')).first()
    password = request.form.get('password')

    if request.method == "GET": #If browser asked to see the page
        return render_template('signin.html', form=form, title='user')

    else:#When the user clicks the sign_in button
        if form.validate_on_submit():
            session.pop('logged_in_user', None)
            #Check if the username/password is matching
            if usern == None and usere == None:
                return render_template('signin.html', form=form, error = 'please check your username/password again')

            else:
                try:
                    passwith = check_password_hash(usern.password, password)                             
                except:
                    passwith = check_password_hash(usere.password, password)
                finally:
                    if not passwith:
                        return render_template('signin.html', form=form, error = 'please check your username/password again') 

            #redirects profile if it matches
            if usere == None:
                session['logged_in_user'] = usern.id
                return redirect(url_for('profile', id=session['logged_in_user']))

            else:
                session['logged_in_user'] = usere.id
                return redirect(url_for('profile', id=session['logged_in_user']))

        else:
            return render_template('signin.html', form=form, title='user')


@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    "Sign up route. Allows you to create a new account with the input information if possible."
    form = Sign_up()
    if request.method == "GET": #If browser asked to see the page
        return render_template('signup.html', form=form, title='sign_up')
    
    #When the user clicks the sign_up button
    else:
        if form.validate_on_submit():
            if models.User.query.filter_by(username = form.username.data).first() != None:
                return render_template('signup.html', form=form, error = 'username already in use')

            if models.User.query.filter_by(email = form.email.data).first() != None:
                return render_template('signup.html', form=form, error = 'email already in use')

            if len(request.form.get('password')) < 8:
                return render_template('signup.html', form=form, error='password must be atleast 8 letters')

            if form.password.data != form.re_password.data:
                return render_template('signup.html', form=form, error = 'your passwords do not match. Please try again')

            else:# if possible, create an account. 
                user_info = models.User(
                    username = form.username.data,
                    email = form.email.data,
                    #Hash the password for extra security
                    password = generate_password_hash(form.password.data, method='sha256')
                )
                db.session.add(user_info)
                db.session.commit()
                
                return redirect(url_for('signin'))
        
        else:
            return render_template('signup.html', form=form, title='sign_up')


@app.route('/logout')
def logout():
    "Route for logout."
    session.pop('logged_in_user', None)

    return redirect(url_for('signin'))


@app.before_request
def before_request():
    "Called before the request, checks if anybody is logged in."
    g.logged_in_user = None
    if 'logged_in_user' in session:
        g.logged_in_user = session['logged_in_user']


@app.errorhandler(404)
def return_error(e):
    return render_template('404.html'), 404
if __name__ == "__main__":
    app.run(debug=True)