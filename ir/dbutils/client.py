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
