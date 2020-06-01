import json
from sqlalchemy.sql import func
from . import app, client, cache, create_token, init_database

class TestAuthrCrud():    
    def test_post_auth_refresh_token(self, client, init_database):
        token = create_token()
        res = client.post('/auth/refresh',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    # def test_post_auth_create_token(self, client, init_database):
    #     token = create_token()
    #     res = client.post('/auth/',
    #                     headers={'Authorization': 'Bearer ' + token},
    #                     content_type='application/json')
        
    #     res_json = json.loads(res.data)
    #     assert res.status_code == 200

    def test_post_auth_create_token_invalid(self, client, init_database):
        token = create_token()
        res = client.get(
            '/auth/100', 
            headers={'Authorization':'Bearer ' + token}, 
            content_type='application/json'
            )
        res_json = json.loads(res.data)
        assert res.status_code == 404