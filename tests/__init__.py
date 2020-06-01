import pytest, json, logging
from flask import Flask, request, json
from blueprints import app
from app import cache, logging
from blueprints.tweet.model import Tweets
from blueprints.follower.model import Followers
from blueprints.user.model import Users
import hashlib, uuid
from blueprints import db

def call_client(request):
    client = app.test_client()
    return client

@pytest.fixture
def client(request):
    return call_client(request)

@pytest.fixture
def init_database():
    
    db.drop_all()
    db.create_all()

    salt = uuid.uuid4().hex
    encoded = ('%s%s' % ("password", salt)).encode('utf-8')
    hash_pass = hashlib.sha512(encoded).hexdigest()

    user_required = Users(name="shofi", username="@shofiya", password=hash_pass, bio="ini shofi", pict_profile="ini pict", pict_bg="ini pict", salt=salt)

    # user_nonrequired = Users(name="noshofi", username="@noshofiya", password=hash_pass, bio="ini shofi", pict_profile="ini pict", pict_bg="ini pict", salt=salt, status="false")

    db.session.add(user_required)
    # db.session.add(user_nonrequired)
    db.session.commit()

    follower = Followers(follower=6, user_id=1)
    tweet = Tweets(tweet="ini twit", user_id=1)
    # db.session.add(user)
    db.session.add(follower)
    db.session.add(tweet)
    db.session.commit()

    yield db

def create_token():
    token = cache.get('test-token')
    if token is None:
        data = {
            'username': '@shofiya',
            'password': 'password'
        }
        req = call_client(request)
        res = req.get('/login?', query_string=data, content_type='application/json')
        res_json = json.loads(res.data)

        logging.warning('RESULT:%s', res_json)

        assert res.status_code == 200

        cache.set('test-token', res_json['token'], timeout=60)

        return res_json['token']
    else:
        return token

