import json
from . import app, client, cache, create_token, init_database

class TestRentCrud():
    id_rent = 0
    def test_rent_list(self, client, init_database):
        token = create_token()
        res = client.get(
            '/rent',
            headers={'Authorization':'Bearer ' + token}, 
            content_type='application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_rent_invalid_get(self, client, init_database):
        token = create_token()
        res = client.get(
            '/rent/100', 
            headers={'Authorization':'Bearer ' + token}, 
            content_type='application/json'
            )
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_rent_insert(self, client, init_database):
        token = create_token()

        data = {
            "user_id": 1,
            "book_id": 1
        }

        res = client.post(
            '/rent', 
            json = data,
            headers={'Authorization': 'Bearer ' + token},
            content_type='application/json'
            )
        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json['id'] > 0
        # self.id_rent = res_json['id']

    def test_rent_id(self, client, init_database):
        token = create_token()
        res = client.get(
            '/rent/1', 
            headers={'Authorization':'Bearer ' + token}, 
            content_type='application/json'
            )
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_filterby(self, client, init_database):
        token = create_token()
        res = client.get(
            '/rent', 
            query_string={
                "orderby": "book_id",
                "sort": "asc"
            },
            headers={'Authorization':'Bearer ' + token}
            )
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_filterby2(self, client, init_database):
        token = create_token()
        res = client.get(
            '/rent', 
            query_string={
                "orderby": "book_id",
                "sort": "desc"
            },
            headers={'Authorization':'Bearer ' + token}
            )
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_filterby3(self, client, init_database):
        token = create_token()
        res = client.get(
            '/rent', 
            query_string={
                "orderby": "user_id",
                "sort": "desc"
            },
            headers={'Authorization':'Bearer ' + token}
            )
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_filterby4(self, client, init_database):
        token = create_token()
        res = client.get(
            '/rent', 
            query_string={
                "orderby": "user_id",
                "sort": "asc"
            },
            headers={'Authorization':'Bearer ' + token}
            )
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_rent_remove(self, client, init_database):
        token = create_token()
        res = client.delete('/rent/1', 
                        headers={'Authorization':'Bearer '+token},
                        content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code==200

    def test_rent_put(self, client, init_database):
        token = create_token()
        data = {     
            "user_id": 1,
            "book_id": 1,
            "return_date": "2001-10-20 13:00:00"
        }

        res = client.put('/rent/1', 
            json=data,
            headers={'Authorization':'Bearer '+token},
        )

        res_json = json.loads(res.data)
        assert res.status_code==200

    def test_rent_update_invalid(self, client, init_database):
        token = create_token()

        data = {
            "user_id": 1,
            "book_id": 1,
            "return_date": "2001-10-20 13:00:00"
        }

        res = client.put(
            '/rent/100', 
            json = data,
            headers={'Authorization': 'Bearer ' + token},
            content_type='application/json'
            )
        res_json = json.loads(res.data)
        assert res.status_code == 404