# import json
# from . import app, client, cache, create_token, init_database

# class TestClientCrud():

#     id_client = 0

#     #get all
#     def test_client_list(self, client, init_database):
#         token = create_token()
#         res = client.get('/client', 
#                         headers={'Authorization':'Bearer '+token},
#                         content_type='application/json')

#         res_json = json.loads(res.data)
#         assert res.status_code==200

#     #post
#     def test_client_insert(self, client, init_database):
#         token = create_token()

#         data = {         
#             "client_key": "ana",
#             "client_secret": "rahasia ilahi",
#             "status": "okelah"
#         }

#         res = client.post('/client',
#                          json=data,
#                          headers={'Authorization': 'Bearer ' + token}
#                          )
#         res_json = json.loads(res.data)
#         assert res.status_code == 200
       
#         self.id_client = res_json['id']

#     #delete
#     def test_client_remove(self, client, init_database):
#         token = create_token()
#         res = client.delete('/client/1', 
#                         headers={'Authorization':'Bearer '+token},
#                         content_type='application/json')

#         res_json = json.loads(res.data)
#         assert res.status_code==200

#     #get by id
#     def test_client_get_by_id(self, client, init_database):
#         token = create_token()
#         res = client.get('/client/1', 
#                         headers={'Authorization':'Bearer '+token},
#                         content_type='application/json')

#         res_json = json.loads(res.data)
#         assert res.status_code==200

#     #put
#     def test_client_put(self, client, init_database):
#         token = create_token()

#         data = {         
#             "client_key": "aisyah",
#             "client_secret": "bukan rahasia ilahi",
#             "status": "okesip"
#         }

#         res = client.put('/client/1', 
#                         json=data,
#                         headers={'Authorization':'Bearer '+token},
#                         )

#         res_json = json.loads(res.data)
#         assert res.status_code==200

#     #untuk yg NOT FOUND
#     def test_client_id_invalid(self, client, init_database):
#         token = create_token()
#         res = client.get(
#             '/client/100', 
#             headers={'Authorization':'Bearer ' + token}, 
#             content_type='application/json'
#             )
#         res_json = json.loads(res.data)
#         assert res.status_code == 404

#     #patch
#     def test_client_patch(self, client, init_database):
#         token = create_token()
#         res = client.patch(
#             '/client',
#             headers={'Authorization':'Bearer ' + token}, 
#             content_type='application/json'
#         )
#         res_json = json.loads(res.data)
#         assert res.status_code == 501

#     def test_get_filterby(self, client, init_database):
#         token = create_token()
#         res = client.get(
#             '/client', 
#             query_string={
#                 "id": 1,
#                 "status": "true",
#                 "orderby": "id",
#                 "sort": "desc"
#             },
#             headers={'Authorization':'Bearer ' + token}
#             )
#         res_json = json.loads(res.data)
#         assert res.status_code == 200

#     def test_get_filterby2(self, client, init_database):
#         token = create_token()
#         res = client.get(
#             '/client', 
#             query_string={
#                 "id": 1,
#                 "status": "false",
#                 "orderby": "id",
#                 "sort": "asc"
#             },
#             headers={'Authorization':'Bearer ' + token}
#             )
#         res_json = json.loads(res.data)
#         assert res.status_code == 200

#     def test_get_filterby3(self, client, init_database):
#         token = create_token()
#         res = client.get(
#             '/client', 
#             query_string={
#                 "id": 1,
#                 "status": "true",
#                 "orderby": "status",
#                 "sort": "desc"
#             },
#             headers={'Authorization':'Bearer ' + token}
#             )
#         res_json = json.loads(res.data)
#         assert res.status_code == 200

#     def test_get_filterby4(self, client, init_database):
#         token = create_token()
#         res = client.get(
#             '/client', 
#             query_string={
#                 "id": 1,
#                 "status": "true",
#                 "orderby": "status",
#                 "sort": "asc"
#             },
#             headers={'Authorization':'Bearer ' + token}
#             )
#         res_json = json.loads(res.data)
#         assert res.status_code == 200

#     def test_client_update_invalid(self, client, init_database):
#         token = create_token()

#         data = {
#             "client_key": "clientheh0",
#             "client_secret": "rahasiaayaa",
#             "status": "True"
#         }

#         res = client.put(
#             '/client/100', 
#             json = data,
#             headers={'Authorization': 'Bearer ' + token},
#             content_type='application/json'
#             )
#         res_json = json.loads(res.data)
#         assert res.status_code == 404

#     def test_client_delete_invalid(self, client, init_database):
#         token = create_token()

#         res = client.delete(
#             '/client/100', 
#             headers={'Authorization': 'Bearer ' + token},content_type='application/json')
#         res_json = json.loads(res.data)
#         assert res.status_code == 404