# coding: utf-8
from datetime import datetime
from app import db
from app import login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Table, Text, Column, ForeignKey
from flask_sqlalchemy import SQLAlchemy # sql operations
from hashlib import md5

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)#f
    email = db.Column(db.String(120), index=True, unique=True)#f
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(150))#f
    area = db.Column(db.String(100))#f
    hability = db.Column(db.String(140))#  f
    course = db.Column(db.String(50))#f
    contact = db.Column(db.String(50))# f
    codecpfcnpj = db.Column(db.String(14))# f
    blocked = db.Column(db.Boolean)# f
    #security_code = db.Column(db.String(255))
    #passwordchangerequest = db.Column(db.Boolean)
    description = db.Column(db.String(140))#
    #token = db.Column(db.String(255))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(str(self.password_hash), password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(250))
    hability = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id =  db.Column(db.Integer, db.ForeignKey('user.id'))
    visibility = db.Column(db.Integer)
    images = db.relationship('Post_Image', backref='post', lazy='dynamic')

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class Post_Image(db.Model):
	__tablename__ = 'post_image'
	id = db.Column(db.Integer, primary_key=True)
	path = db.Column(db.String(255))
	post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
	def __init__(self, path, post):
		self.path=path;
		self.post=post;
	def __repr__(self):
		return '<Post_Images path:%r>' % self.path


db.create_all();
