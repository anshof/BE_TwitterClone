import json
import config
import os
from functools import wraps
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
from flask_cors import CORS

app = Flask(__name__)

jwt = JWTManager(app)

app.config['APP_DEBUG'] = True
CORS(app, origins="*", allow_headers=[
    "Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
    supports_credentials=True, intercept_exceptions=False)

def user_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['status'] != 'true':
            return {'status': 'FORBIDDEN', 'message': 'User Only!'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper

flask_env = os.environ.get('FLASK_ENV', 'Production')
if flask_env == 'Production':
    app.config.from_object(config.ProductionConfig)
elif flask_env == "Testing":
    app.config.from_object(config.TestingConfig)
else:
    app.config.from_object(config.DevelopmentConfig)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@app.after_request
def after_request(response):
    try:
        requestData = request.get_json()
    except Exception as e:
        requestData = request.args.to_dict()
    if response.status_code == 200:
        app.logger.warning("REQUEST_LOG\t%s", json.dumps({
            'method': request.method,
            'code': response.status,
            'uri': request.full_path,
            'request': requestData,
            'response': json.loads(response.data.decode('utf-8'))}))
    else:
        app.logger.warning("REQUEST_LOG\t%s", json.dumps({
            'method': request.method,
            'code': response.status,
            'uri': request.full_path,
            'request': requestData,
            'response': json.loads(response.data.decode('utf-8'))}))

    return response

    @app.before_request
    def before_request():
        if request.method != 'OPTIONS':
            pass
        else:
            return {}, 200, {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*'}
from blueprints.user.resources import bp_user
from blueprints.login import bp_login
from blueprints.tweet.resources import bp_tweet
from blueprints.follower.resources import bp_follower


app.register_blueprint(bp_user, url_prefix='/user')
app.register_blueprint(bp_login, url_prefix='/login')
app.register_blueprint(bp_tweet, url_prefix='/tweet')
app.register_blueprint(bp_follower, url_prefix='/follower')

db.create_all()
