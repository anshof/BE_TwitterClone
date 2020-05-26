from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from ..user.model import Users
import hashlib
import uuid

bp_login = Blueprint('login', __name__)
api = Api(bp_login)


class CreateTokenResource(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='args', required=True)
        parser.add_argument('password', location='args', required=True)
        args = parser.parse_args()

        qry_user = Users.query.filter_by(
            username=args['username']).first()

        if qry_user is not None:
            user_salt = qry_user.salt

            encoded = ('%s%s' %
                       (args['password'], user_salt)).encode('utf-8')
            hash_pass = hashlib.sha512(encoded).hexdigest()
            if hash_pass == qry_user.password and qry_user.username == args['username']:
                qry_user = marshal(qry_user, Users.jwt_claim_fields)
                qry_user['identifier'] = "shofiya"
                token = create_access_token(
                    identity=args['username'], user_claims=qry_user)
                return {'token': token}, 200
        return {'status': 'UNAUTHORIZED', 'message': 'invalid username or password'}, 404

    def options(self):
        return{}, 200
        
api.add_resource(CreateTokenResource, '')
