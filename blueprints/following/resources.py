import json
import hashlib
import uuid
from flask import Blueprint
from flask_restful import Api, Resource, marshal, reqparse, inputs
from .model import Following
from blueprints.user.model import Users

from blueprints import db, app
from sqlalchemy import desc
from blueprints import user_required
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

bp_following = Blueprint('following', __name__)
api = Api(bp_tweet)


class FollowerResource(Resource):
    def __init__(self):
        pass

    def get(self, id):
        qry = Followers.query.get(id)
        if qry is not None:
            return marshal(qry, Followers.response_field), 200
        return {'status': 'NOT_FOUND'}, 404

    @user_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('follower', location='json', required=True)
        args = parser.parse_args()

        claims = get_jwt_claims()
        print(claims['id'])
        qry = Users.query.filter_by(user_id=claims["id"]).first()
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

    @seller_required
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

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('follower', location='args')
       
        parser.add_argument('orderby', location='args', help='invalid orderby value')
        parser.add_argument('sort', location='args',
                            help='invalid sort value', choices=('desc', 'asc'))

        args = parser.parse_args()
        offset = (args['p'] * args['rp']) - args['rp']
        qry = Followers.query

        if args['follower'] is not None:
            qry = qry.filter_by(name=args['follower'])

        if args['orderby'] is not None:
            if args['orderby'] == 'follower':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Followers.follower))
                else:
                    qry = qry.order_by(Followers.follower)

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Followers.response_field))

        return rows, 200

    def options(self):
        return{}, 200

api.add_resource(FollowerList, '', '')
api.add_resource(FollowerResource, '', '/<id>')
