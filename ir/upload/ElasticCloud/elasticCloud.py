from elasticsearch import Elasticsearch

client = Elasticsearch(
    "https://67019a3983704628b6f2625991800058.us-central1.gcp.cloud.es.io:443",
    api_key="RGhjbS1JNEJrd3BZN2ZlMmxCQy06bTZyZnhzbkdUVWFTSkJ0dDZEWlRvQQ=="
)

# # data = {
# #     'title': 'The Lord of the Rings',
# #     'author': 'J.R.R. Tolkien',
# #     'year': 1954,
# #     'quote': 'Not all who wander are lost.'
# # }

# print(client.info(),'= info')

# mapping = {
#     'properties': {
#         'documentid': {'type': 'text'},
#         'file_name': {'type': 'text'},
#         'file_loc': {'type': 'text'},
#         'content': {'type': 'text'},
#         'position_index': {'type': 'object'},
#         'type': {'type': 'text'},
#         'created_at':{'type': 'date'}
#     }
# }

# index_name = 'ir_project'


# client.indices.create(index=index_name, body={'mappings': mapping})