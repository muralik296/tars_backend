import os
from dotenv import load_dotenv

load_dotenv()
from elasticsearch import Elasticsearch


ELASTIC_SEARCH_SERVER = os.getenv("ELASTIC_SEARCH_SERVER")
ELASTIC_SEARCH_API_KEY = os.getenv("ELASTIC_SEARCH_API_KEY")

client = Elasticsearch(
    ELASTIC_SEARCH_SERVER,
    api_key=ELASTIC_SEARCH_API_KEY
)

mapping_pos_index = {
    'properties': {
        'positional_index': {'type': 'object', 'enabled': 'false'}
    }
}

mapping_main = {
    'properties': {
        'content': {'type': 'text'},
        'created_at': {'type': 'date'},
        'documentid': {'type': 'text'},
        'file_loc': {'type': 'text'},
        'file_name': {'type': 'text'},
        'type': {'type': 'text'},
        'posting_list':{'type':'object','enabled':'false'}
    }
}

main_index = 'main'
positional_index_index = 'positional_index'

# main index
client.indices.create(index=main_index, body={'mappings': mapping_main})

# positional index
client.indices.create(index=positional_index_index, body={'mappings': mapping_pos_index})

