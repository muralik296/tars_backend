# this file has all operations related to index 'positional_index'

from .elasticCloud import client

index = 'positional_index'

# helper to check if the positional index is stored in the database


def get_positional_index():
    ''' Returns positional index record with id = 1'''
    res = client.get(index=index, id=1)
    return res


def insert_into_positional_index_index(posting_list):
    ''' Saves posting list into positional index index '''
    response = client.index(
        index=index,
        document={
            'positional_index': posting_list
        },
        id=1)
    return response


def update_positional_index(doc):
    ''' Updates the index with element '''
    response = client.update(
        index=index,
        id=1,
        body={
            'doc': doc
        }
    )
    return response


def check_document_exists():
    '''Checks if document with id 1 exists '''
    try:
        exists = client.exists(index=index, id=1)
        return exists
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
