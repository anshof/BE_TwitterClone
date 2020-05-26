from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
from sqlalchemy.orm import relationship

class Users(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    salt = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    pict_profile = db.Column(db.String(255), default="https://pbs.twimg.com/profile_images/3182474033/c1d33595bce12b515bb83197eab2d9ba_400x400.jpeg")
    pict_bg = db.Column(db.String(255), default="https://pbs.twimg.com/profile_images/3182474033/c1d33595bce12b515bb83197eab2d9ba_400x400.jpeg")
    follower = db.Column(db.Integer, default=0)
    following = db.Column(db.Integer, default=0)
    status = db.Column(db.String(10), default='true')
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())

    tweets = db.relationship('Tweets', backref='user', lazy=True)

    response_field = {
        'id': fields.Integer,
        'name': fields.String,
        'username': fields.String,
        'password': fields.String,
        'bio': fields.String,
        'pict_profile': fields.String,
        'pict_bg': fields.String,
        'follower':fields.Integer,
        'following':fields.Integer,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }
    jwt_claim_fields = {
        'id': fields.Integer,
        'username': fields.String,
        'status': fields.String
    }

    def __init__(self, name, username, password, bio, pict_profile, pict_bg, salt):
        self.name = name
        self.username = username
        self.password = password
        self.bio = bio
        self.pict_profile = pict_profile
        self.pict_bg = pict_bg
        self.salt = salt

    def __repr__(self):
        return '<User %r>' % self.id
