# import json
# from . import app, client, cache, create_token, init_database

# class TestBookCrud():
#     id_book = 0
#     #get all
#     def test_book_list(self, client, init_database):
#         token = create_token()
#         res = client.get('/book', 
#             headers={'Authorization':'Bearer '+token},
#             content_type='application/json')

#         res_json = json.loads(res.data)
#         assert res.status_code==200

#     #post
#     def test_book_insert(self, client, init_database):
#         token = create_token()

#         data = {
#                 "title": "Judul Buku Empat",
#                 "isbn": "1-234-5678-910112-13",
#                 "writer": "Dumbledore"
#                 }
#         res = client.post('/book',
#                          json=data,
#                          headers={'Authorization': 'Bearer ' + token}
#                          )
#         res_json = json.loads(res.data)
#         assert res.status_code == 200

#     #get by id
#     def test_book_get_by_id(self, client, init_database):
#         token = create_token()
#         res = client.get('/book/1', 
#                         headers={'Authorization':'Bearer '+token},
#                         content_type='application/json')

#         res_json = json.loads(res.data)
#         assert res.status_code==200

#     #put
#     def test_book_put(self, client, init_database):
#         token = create_token()

#         data = {
#             "title": "Judul Buku Lima",
#             "isbn": "1-234-5678-9101112-14",
#             "writer": "Dr. What"
#             }
        

#         res = client.put('/book/1', 
#                         json=data,
#                         headers={'Authorization':'Bearer '+token},
#                         )
#     #delete
#     def test_book_remove(self, client, init_database):
#         token = create_token()
#         res = client.delete('/book/1', 
#                         headers={'Authorization':'Bearer '+token},
#                         content_type='application/json')

#         res_json = json.loads(res.data)
#         assert res.status_code==200

#     #untuk yg NOT FOUND
#     def test_book_id_invalid(self, client, init_database):
#         token = create_token()
#         res = client.get(
#             '/book/100', 
#             headers={'Authorization':'Bearer ' + token}, 
#             content_type='application/json'
#             )
#         res_json = json.loads(res.data)
#         assert res.status_code == 404

#     #put invalid
#     def test_book_update_invalid(self, client, init_database):
#         token = create_token()

#         data = {
#             "title": "coba ganty213475",
#             "isbn": "081-32000",
#             "writer": "Kak Rose"
#         }

#         res = client.put(
#             '/book/100', 
#             json = data,
#             headers={'Authorization': 'Bearer ' + token},
#             content_type='application/json'
#             )
#         res_json = json.loads(res.data)
#         assert res.status_code == 404

#     #delete invalid
#     def test_book_remove_invalid(self, client, init_database):
#         token = create_token()
#         res = client.delete(
#             '/book/100', 
#             headers={'Authorization':'Bearer ' + token}, 
#             content_type='application/json'
#             )
#         res_json = json.loads(res.data)
#         assert res.status_code == 404


#     #patch
#     def test_book_patch(self, client, init_database):
#         token = create_token()
#         res = client.patch(
#             '/book',
#             headers={'Authorization':'Bearer ' + token}, 
#             content_type='application/json'
#         )
#         res_json = json.loads(res.data)
#         assert res.status_code == 501

#     def test_get_filterby(self, client, init_database):
#         token = create_token()
#         res = client.get(
#             '/book', 
#             query_string={
#                 "title": "oci",
#                 "isbn": "101010",
#                 "orderby": "title",
#                 "sort": "desc"
#             },
#             headers={'Authorization':'Bearer ' + token}
#             )
#         res_json = json.loads(res.data)
#         assert res.status_code == 200

#     def test_get_filterby2(self, client, init_database):
#         token = create_token()
#         res = client.get(
#             '/book', 
#             query_string={
#                 "title": "oci",
#                 "isbn": "101010",
#                 "orderby": "title",
#                 "sort": "asc"
#             },
#             headers={'Authorization':'Bearer ' + token}
#             )
#         res_json = json.loads(res.data)
#         assert res.status_code == 200

#     def test_get_filterby3(self, client, init_database):
#         token = create_token()
#         res = client.get(
#             '/book', 
#             query_string={
#                 "title": "oci",
#                 "isbn": "101010",
#                 "orderby": "isbn",
#                 "sort": "asc"
#             },
#             headers={'Authorization':'Bearer ' + token}
#             )
#         res_json = json.loads(res.data)
#         assert res.status_code == 200

#     def test_get_filterby4(self, client, init_database):
#         token = create_token()
#         res = client.get(
#             '/book', 
#             query_string={
#                 "title": "oci",
#                 "isbn": "101010",
#                 "orderby": "isbn",
#                 "sort": "desc"
#             },
#             headers={'Authorization':'Bearer ' + token}
#             )
#         res_json = json.loads(res.data)
#         assert res.status_code == 200