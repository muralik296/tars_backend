from .elasticCloud import client

index = 'main'


def insert_into_main(document):
    # saves the document in the index main
    res = client.index(
        index=index,
        document=document)
    client.indices.refresh(index=index)
    return res
    
