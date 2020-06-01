import json
import hashlib
import uuid
from flask import Blueprint
from flask_restful import Api, Resource, marshal, reqparse, inputs
from .model import Followers
from blueprints.user.model import Users

from numpy import *
from blueprints import db, app
from sqlalchemy import desc
from blueprints import user_required
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

bp_follower = Blueprint('follower', __name__)
api = Api(bp_follower)


class FollowerResource(Resource):
    def __init__(self):
        pass

    # get follower
    @user_required
    def get(self):
        claims = get_jwt_claims()
        qry = Users.query.filter_by(id=claims["id"]).first()
        user_id=qry.id

        print("+++++", qry)

        follow = Followers.query.filter_by(user_id=user_id).all()

        rows = []
        for row in follow:
            user = Users.query.filter_by(id=row.follower).first()
            marshalUser = marshal(user, Users.response_field)
            marshalqry = marshal(row, Followers.response_field)

            marshalqry["follower"]=marshalUser
            rows.append(marshalqry)
        return rows, 200

    # post follower
    @user_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('follower', location='json', required=True)
        args = parser.parse_args()

        claims = get_jwt_claims()
        print(claims['id'])
        qry = Users.query.filter_by(id=claims["id"]).first()
        print(qry)
        user_id = qry.id

        follower = Followers(args['follower'], user_id)
        db.session.add(follower)
        db.session.commit()
        app.logger.debug('DEBUG: %s', follower)

        return marshal(follower, Followers.response_field), 200, {'Content-Type': 'application/json'}

    @user_required
    def patch(self, id):

        parser = reqparse.RequestParser()
        parser.add_argument('follower', location='json', required=True)
        args = parser.parse_args()

        claims = get_jwt_claims()
        qry_user = Users.query.filter_by(user_id=claims['id'])
        user_id = qry_user.id
        qry_tweet = Followers.query.filter_by(user_id=user_id).all()
        qry = qry_tweet.get(id)

        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        qry.follower = args['follower']
        db.session.commit()

        return marshal(follower, Followers.response_field), 200

    def delete(self, id):
        claims = get_jwt_claims()
        qry_user = Users.query.filter_by(user_id=claims['id']).first()
        user_id = qry_user.id
        qry_tweet = Followers.query.filter_by(user_id=user_id)

        qry = qry_tweet.filter_by(id=id).first()
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()
        return {'status': 'DELETED'}, 200

    def options(self):
        return{}, 200

class FollowerList(Resource):
    def __init__(self):
        pass

    # get user we follow
    @user_required
    def get(self):
        claims = get_jwt_claims()
        qry = Users.query.filter_by(id=claims["id"]).first()
        user_id=qry.id

        follow = Followers.query.filter_by(user_id=user_id).all()
        rows = []
        for row in follow:
            follower_id=row.follower
            rows.append(follower_id)
     
        user = Users.query.filter(~Users.id.in_(rows)).filter(Users.id!=claims['id']).all()

        return marshal(user, Users.response_field), 200

    def options(self):
        return{}, 200

class Following(Resource):
    def __init__(self):
        pass

    @user_required
    def get(self):
        claims = get_jwt_claims()
        qry = Users.query.filter_by(id=claims["id"]).first()
        user_id=qry.id

        print("+++++", qry)

        follow = Followers.query.filter_by(follower=user_id).all()

        rows = []
        for row in follow:
            user = Users.query.filter_by(id=row.follower).first()
            marshalUser = marshal(user, Users.response_field)
            marshalqry = marshal(row, Followers.response_field)

            marshalqry["follower"]=marshalUser
            rows.append(marshalqry)
        return rows, 200

    def options(self):
        return{}, 200

api.add_resource(Following, '/follow')
api.add_resource(FollowerList, '/list')
api.add_resource(FollowerResource, '', '/<id>')
