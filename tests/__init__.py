import pytest, json, logging
from flask import Flask, request, json
from blueprints import app
from app import cache, logging
from blueprints.client.model import Clients
from blueprints.user.model import Users
from blueprints.book.model import Books
from blueprints.rent.model import Rents
# from blueprints.auth import auth
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

    client_internal = Clients(client_key="internal", client_secret=hash_pass, status="True", salt=salt)
    client_noninternal = Clients(client_key="noninternal", client_secret=hash_pass, status="False", salt=salt)
    db.session.add(client_internal)
    db.session.add(client_noninternal)
    db.session.commit()

    user = Users(name="shofi", age=25, sex="female", client_id=1)
    book = Books(title="shofiya", isbn="123-456", writer="tere liye")
    db.session.add(user)
    db.session.add(book)
    db.session.commit()

    rent = Rents(user_id=1, book_id=1, return_date="01:10:20.000013")
    db.session.add(rent)
    db.session.commit()

    yield db

def create_token():
    token = cache.get('test-token')
    if token is None:
        data = {
            'client_key': 'internal',
            'client_secret': 'password'
        }
        req = call_client(request)
        res = req.get('/auth?', query_string=data, content_type='application/json')
        res_json = json.loads(res.data)

        logging.warning('RESULT:%s', res_json)

        assert res.status_code == 200

        cache.set('test-token', res_json['token'], timeout=60)

        return res_json['token']
    else:
        return token

