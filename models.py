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
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    email = db.Column(db.Text)
    password = db.Column(db.Text)

    posts_user = db.relationship('Post', secondary=PostUser, back_populates='users_post')
    notifications_user = db.relationship('Notification', secondary=UserNotification, back_populates='users_notification')


class Reply(db.Model):
    __tablename__ = 'Reply'
    id = db.Column(db.Integer, primary_key=True)
    reply = db.Column(db.Text)
    date = db.Column(db.Integer)

    posts_reply = db.relationship('Post', secondary=PostReply, back_populates='replies_post')


class Post(db.Model):
    __tablename__ = 'Post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    discussion = db.Column(db.Text)
    date = db.Column(db.Integer)
    likes = db.Column(db.Integer)

    users_post = db.relationship('User', secondary=PostUser, back_populates='posts_user')
    replies_post = db.relationship('Reply', secondary=PostReply, back_populates='posts_reply')
    categories_post = db.relationship('Categories', secondary=PostCategory, back_populates='posts_category')


class Notification(db.Model):
    __tablename__ = 'Notification'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    content = db.Column(db.Text)

    users_notification = db.relationship('User', secondary=UserNotification, back_populates='notifications_user')


class Categories(db.Model):
    __tablename__ = 'Categories'
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.Text)

    posts_category = db.relationship('Post', secondary=PostCategory, back_populates='categories_post')

