# this file has all operations related to index 'positional_index'

from .elasticCloud import client

index = 'positional_index'

# helper to check if the positional index is stored in the database


def get_positional_index():
    ''' Returns positional index record with id = 1'''
    res = client.search(
        index=index,
        query={
            'match': {'id': {
                'query': 1
            }}
        })
    return res


def insert_into_positional_index_index(posting_list):
    ''' Saves posting list into positional index index '''
    response = client.index(
        index=index,
        document={
            'id': 1,
            'positional_index': posting_list
        })
    return response


def update_positional_index(id, doc):
    ''' Updates the index with element '''
    response = client.update(
        index=index,
        id=id,
        body={
            'doc': doc
        }
    )
    return response
