from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref


class Followers(db.Model):
    __tablename__ = 'follower'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    follower = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    response_field = {
        'id': fields.Integer,
        'user_id': fields.Integer,
        'follower': fields.Integer,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime,
    }

    def __init__(self, follower, user_id):
        self.follower = follower
        self.user_id = user_id

    def __repr__(self):
        return '<Follower %r>' % self.id
