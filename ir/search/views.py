# Create your views here.
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import json

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError, ConnectionError, TransportError

from dbutils import positional_index

from dbutils import main

from .search_algo import return_docs

index_name = 'ir_project'


@csrf_exempt
def searchHandler(request):
    try:
        if (request.method == 'POST'):
            requestBody = json.loads(request.body)
            search_query = requestBody['query']
            search_query = search_query.lower()
            print(search_query, '= search query')

            search_queries = search_query.split(
                ',')  # support for free queries
            print(search_queries, 'search queries')

            # checking if positional index exists, if not then return an empty search result
            if (positional_index.check_document_exists() == False):
                return JsonResponse({
                    'data': []
                }, status=201)

            document_ids = []
            for search_query in search_queries:

                result_from_elastic_search = positional_index.get_positional_index()
                pos_index = result_from_elastic_search['_source']['positional_index']

                result = return_docs(pos_index, search_query)
                print(result, f'result for {search_query}')
                document_ids.extend(list(result.keys()))
            
            # removes duplicates incase, the free query search has same document to show for multiple searches
            document_ids = list(set(document_ids))

            print(document_ids, '= document ids')
            if (len(document_ids) == 0):
                    return JsonResponse({
                        'data': []
                    })
            result_from_es_main = main.get_multiple_documents(document_ids)

            # use the search query to perform the phrase query search
            return JsonResponse({
                'data': result_from_es_main['docs']
            }, status=201)
    except Exception as e:
        print(e, '= error')
        return JsonResponse({
            'msg': 'An Error Occurred'
        }, status=500)


def getDocumentById(request, documentId):
    print(documentId, '=documentid')
    try:
        result = main.get_single_document_by_id(documentId)
        print(result, '= result')
        print(result['_source'])
        return JsonResponse({"data": result['_source']}, status=200)

    except NotFoundError as e:
        print("The document or index specified does not exist.")
        print(e, '= error')
        return JsonResponse({
            'msg': f'Document with {documentId} not found.'
        }, status=404)
    except Exception as e:
        print(e, '=error')
        return JsonResponse({
            'msg': 'An error occured'
        }, status=500)


@csrf_exempt
def get_posting_list_for_phrase(request):
    if (request.method == 'POST'):
        requestBody = json.loads(request.body)
        search_query = requestBody['query']
        print(search_query, '= search query')
        positional_index = positional_index.get_positional_index()
        pos_index = positional_index['hits']['hits'][0]['_source']['positional_index']
        print(pos_index, '=res')

        result = return_docs(pos_index, search_query)
        return JsonResponse({
            "data": [result]
        })
