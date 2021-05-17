from main import db


PostCategory = db.Table('PostCategory', db.Model.metadata, 
                    db.Column('Post_id', db.Integer, db.ForeignKey('Post.id')), 
                    db.Column('Categories_id', db.Integer, db.ForeignKey('Categories.id')))


PostReply = db.Table('PostReply', db.Model.metadata, 
                    db.Column('Post_id', db.Integer, db.ForeignKey('Post.id')), 
                    db.Column('Reply_id', db.Integer, db.ForeignKey('Reply.id')))


UserNotification = db.Table('UserNotification', db.Model.metadata, 
                    db.Column('User_id', db.Integer, db.ForeignKey('User.id')), 
                    db.Column('Notification_id', db.Integer, db.ForeignKey('Notification.id')))


PostUser = db.Table('PostUser', db.Model.metadata, 
                    db.Column('Post_id', db.Integer, db.ForeignKey('Post.id')), 
                    db.Column('User_id', db.Integer, db.ForeignKey('User.id')))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    email = db.Column(db.Text)
    password = db.Column(db.Text)



class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reply = db.Column(db.Text)
    date = db.Column(db.Integer)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    discussion = db.Column(db.Text)
    date = db.Column(db.Integer)
    likes = db.Column(db.Integer)


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    content = db.Column(db.Text)


class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.Text)

