import json
from . import app, client, cache, create_token, init_database

class TestUserCrud():
    #get all
    def test_user_list(self, client, init_database):
        token = create_token()
        res = client.get('/user', 
            headers={'Authorization':'Bearer '+token},
            content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code==200

    #post
    def test_user_insert(self, client, init_database):

        data = {
                "name": "bagas",
                "username":"@bagas",
                "password":"alta123",
                "bio":"ini bagas",
                "pict_profile":"ini pict",
                "pict_bg":"ini pict",
                }
        res = client.post('/user', json=data, content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200
        self.id_user = res_json['id']

    #get by id
    # def test_user_get_by_id(self, client, init_database):
    #     token = create_token()
    #     res = client.get('/user/1', 
    #                     headers={'Authorization':'Bearer '+token},
    #                     content_type='application/json')

    #     res_json = json.loads(res.data)
    #     assert res.status_code==200

    #put
    def test_user_put(self, client, init_database):
        token = create_token()

        data = {
                "name": "Upin",
                "username":"@upin",
                "password":"alta123",
                "bio":"ini upin",
                "pict_profile":"ini pict",
                "pict_bg":"ini pict",
                }      
        res = client.patch('/user/1', json=data, headers={'Authorization':'Bearer '+token}, content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    #delete
    def test_user_remove(self, client, init_database):
        token = create_token()
        res = client.delete('/user/1', 
                        headers={'Authorization':'Bearer '+token},
                        content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code==200

    # untuk yg NOT FOUND
    # def test_user_id_invalid(self, client, init_database):
    #     token = create_token()
    #     res = client.get(
    #         '/user/100', 
    #         headers={'Authorization':'Bearer ' + token}, 
    #         content_type='application/json'
    #         )
    #     res_json = json.loads(res.data)
    #     assert res.status_code == 404

    #delete invalid
    def test_user_remove_invalid(self, client, init_database):
        token = create_token()
        res = client.delete(
            '/user/100', 
            headers={'Authorization':'Bearer ' + token}, 
            content_type='application/json'
            )
        res_json = json.loads(res.data)
        assert res.status_code == 404

    #put invalid
    def test_user_update_invalid(self, client, init_database):
        token = create_token()
        data = {
               "name": "Upin",
                "username":"@upin",
                "password":"alta123",
                "bio":"ini upin",
                "pict_profile":"ini pict",
                "pict_bg":"ini pict",
        }
        res = client.patch(
            '/user/100', 
            json = data,
            headers={'Authorization': 'Bearer ' + token},
            content_type='application/json'
            )
        res_json = json.loads(res.data)
        assert res.status_code == 404



    # def test_get_filterby(self, client, init_database):
    #     token = create_token()
    #     res = client.get(
    #         '/user', 
    #         query_string={
    #             "sex": "female",
    #             "orderby": "age",
    #             "sort": "desc"
    #         },
    #         headers={'Authorization':'Bearer ' + token}
    #         )
    #     res_json = json.loads(res.data)
    #     assert res.status_code == 200

    # def test_get_filterby2(self, client, init_database):
    #     token = create_token()
    #     res = client.get(
    #         '/user', 
    #         query_string={
    #             "sex": "female",
    #             "orderby": "sex",
    #             "sort": "desc"
    #         },
    #         headers={'Authorization':'Bearer ' + token}
    #         )
    #     res_json = json.loads(res.data)
    #     assert res.status_code == 200

    # def test_get_filterby3(self, client, init_database):
    #     token = create_token()
    #     res = client.get(
    #         '/user', 
    #         query_string={
    #             "sex": "male",
    #             "orderby": "age",
    #             "sort": "asc"
    #         },
    #         headers={'Authorization':'Bearer ' + token}
    #         )
    #     res_json = json.loads(res.data)
    #     assert res.status_code == 200

    # def test_get_filterby4(self, client, init_database):
    #     token = create_token()
    #     res = client.get(
    #         '/user', 
    #         query_string={
    #             "sex": "male",
    #             "orderby": "sex",
    #             "sort": "asc"
    #         },
    #         headers={'Authorization':'Bearer ' + token}
    #         )
    #     res_json = json.loads(res.data)
    #     assert res.status_code == 200