import os
from elasticsearch import Elasticsearch

ELASTIC_SEARCH_SERVER = os.getenv("ELASTIC_SEARCH_SERVER")
ELASTIC_SEARCH_API_KEY = os.getenv("ELASTIC_SEARCH_API_KEY")

client = Elasticsearch(
    ELASTIC_SEARCH_SERVER,
    api_key=ELASTIC_SEARCH_API_KEY
)

# # data = {
# #     'title': 'The Lord of the Rings',
# #     'author': 'J.R.R. Tolkien',
# #     'year': 1954,
# #     'quote': 'Not all who wander are lost.'
# # }

print(client.info(),'= client info')

# mapping = {
#     'properties': {
#         'positional_index': {'type': 'object', 'enabled': 'false'}
#     }
# }

# mapping = {
#     'properties': {
#         'content': {'type': 'text'},
#         'created_at': {'type': 'date'},
#         'documentid': {'type': 'text'},
#         'file_loc': {'type': 'text'},
#         'file_name': {'type': 'text'},
#         'type': {'type': 'text'},
#         'posting_list':{'type':'object','enabled':'false'}
#     }
# }

# index_name = 'main'


# client.indices.create(index=index_name, body={'mappings': mapping})


# testing SOMETHING HERE
# result = client.search(
#     index='pos_index',
#     query={
#         'match': {'id': {
#             'query': 1
#         }}
#     })

# print(result)
# print(result['hits']['hits'])
