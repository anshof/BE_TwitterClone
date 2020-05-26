import json
import hashlib
import uuid
from flask import Blueprint
from flask_restful import Api, Resource, marshal, reqparse, inputs
from .model import Tweets
from blueprints.user.model import Users

from blueprints import db, app
from sqlalchemy import desc
from blueprints import user_required
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

bp_tweet = Blueprint('tweet', __name__)
api = Api(bp_tweet)


class TweetResource(Resource):
    def __init__(self):
        pass

    def get(self, id):
        qry = Tweets.query.get(id)
        if qry is not None:
            return marshal(qry, Tweets.response_field), 200
        return {'status': 'NOT_FOUND'}, 404

    @user_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('tweet', location='json', required=True)
        args = parser.parse_args()

        claims = get_jwt_claims()
        print(claims['id'])
        print('=====', claims)
        qry = Users.query.filter_by(id=claims["id"]).first()
        print(qry)
        user_id = qry.id

        tweet = Tweets(args['tweet'], user_id)
        db.session.add(tweet)
        db.session.commit()
        app.logger.debug('DEBUG: %s', tweet)

        return marshal(tweet, Tweets.response_field), 200, {'Content-Type': 'application/json'}

    @user_required
    def patch(self, id):

        parser = reqparse.RequestParser()
        parser.add_argument('tweet', location='json', required=True)
        args = parser.parse_args()

        qry_tweet = Tweets.query.get(id)

        if qry_tweet is None:
            return {'status': 'NOT_FOUND'}, 404

        qry_tweet.tweet = args['tweet']
        db.session.commit()

        return marshal(qry_tweet, Tweets.response_field), 200

    @user_required
    def delete(self, id):
        claims = get_jwt_claims()
        qry_user = Users.query.filter_by(id=claims['id']).first()
        user_id = qry_user.id
        qry_tweet = Tweets.query.filter_by(user_id=user_id)

        qry = qry_tweet.filter_by(id=id).first()
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()
        return {'status': 'DELETED'}, 200

    def options(self):
        return{}, 200

class TweetList(Resource):
    def __init__(self):
        pass

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('tweet', location='args')
        # parser.add_argument('sort', location='args',help='invalid sort value', choices=('desc', 'asc'))
        
        args = parser.parse_args()
        qry = Tweets.query

        if args['tweet'] is not None:
            qry = qry.filter_by(name=args['tweet'])

        rows = []
        for row in qry.all():
            user = Users.query.filter_by(id=row.user_id).first()
            marshalUser = marshal(user, Users.response_field)
            marshalqry = marshal(row, Tweets.response_field)
            marshalqry["user_id"]=marshalUser
            rows.append(marshalqry)
        return rows, 200

    def options(self):
        return{}, 200

api.add_resource(TweetList, '', '')
api.add_resource(TweetResource, '', '/<id>')