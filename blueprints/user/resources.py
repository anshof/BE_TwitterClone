import json
import hashlib
import uuid
from flask import Blueprint
from flask_restful import Api, Resource, marshal, reqparse, inputs
from .model import Users
from blueprints import db, app, user_required
from sqlalchemy import desc
from blueprints.tweet.model import Tweets
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
bp_user = Blueprint('user', __name__)

api = Api(bp_user)


class UserResource(Resource):
    def __init__(self):
        pass

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        parser.add_argument('bio', location='json')
        parser.add_argument('pict_profile', location='json')
        parser.add_argument('pict_bg', location='json')

        data = parser.parse_args()

        salt = uuid.uuid4().hex
        encoded = ('%s%s' % (data['password'], salt)).encode('utf-8')
        hash_pass = hashlib.sha512(encoded).hexdigest()

        user = Users(data['name'], data['username'], hash_pass, data['bio'], data['pict_profile'], data['pict_bg'], salt)

        db.session.add(user)
        db.session.commit()
        app.logger.debug('DEBUG: %s', user)

        return marshal(user, Users.response_field), 200, {'Content-Type': 'application/json'}

    @user_required
    def get(self):
        claims = get_jwt_claims()
        qry = Users.query.filter_by(id=claims['id']).first()
        if qry is not None:
            return marshal(qry, Users.response_field), 200
        return {'status': 'NOT_FOUND'}, 404  

    @user_required
    def patch(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json')
        parser.add_argument('username', location='json')
        parser.add_argument('password', location='json')
        parser.add_argument('bio', location='json')
        parser.add_argument('follower', location='json')
        parser.add_argument('following', location='json')  
        parser.add_argument('pict_profile', location='json')
        parser.add_argument('pict_bg', location='json')

        data = parser.parse_args()

        qry = Users.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        salt = uuid.uuid4().hex
        encoded = ('%s%s' % (data['password'], salt)).encode('utf-8')
        hash_pass = hashlib.sha512(encoded).hexdigest()
        
        qry.name = data['name']
        qry.username = data['username']
        qry.bio = data['bio']
        qry.follower = data['follower']
        qry.following = data['following']
        qry.pict_profile = data['pict_profile']
        qry.pict_bg = data['pict_bg']
        qry.password = hash_pass
        qry.salt = salt

        db.session.commit()

        return marshal(qry, Users.response_field), 200

    @user_required
    def delete(self, id):
        qry = Users.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        tweets = Tweets.query.filter_by(user_id=id)
        
        for tweet in tweets:
            db.session.delete(tweet)
            db.session.commit()

        db.session.delete(qry)
        db.session.commit()
        return {'status': 'DELETED'}, 200

    def options(self):
        return{}, 200

api.add_resource(UserResource, '', '/<id>')

