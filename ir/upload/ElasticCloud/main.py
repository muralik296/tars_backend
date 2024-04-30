from .elasticCloud import client
from elasticsearch.helpers import bulk

index = 'main'


def insert_into_main(document, documentid):
    ''' Inserts document into main index '''
    res = client.index(
        index=index,
        document=document,
        id=documentid)
    client.indices.refresh(index=index)
    return res


def get_multiple_documents(document_ids):
    ''' Returns multiple docs '''
    response = client.mget(index=index, body={"ids": document_ids})
    return response

def get_single_document_by_id(documentid):
    '''Returns single document with id = document id'''
    response = client.get(index=index,
                            id=documentid)
    return response

def bulk_insert(documents):
    ''' Bulk insert documents into index '''
    response = bulk(client,documents)
    return response