from flask import Flask, render_template
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
    return render_template('home.html', title='home')

@app.route('/post/')
def post():
    return render_template('post.html', title='post')

@app.route('/noti/<int:id>')
def noti(id):
    return render_template('noti.html', title='noti')

@app.route('/profile/<int:id>')
def user(id):
    return render_template('profile.html', title='profile')

@app.route('/signup/')
def signup():
    return render_template('signup.html',title='signup')

if __name__ == "__main__":
    app.run(debug=True)