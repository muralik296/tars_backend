# Create your views here.
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import json

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError, ConnectionError, TransportError

from upload.ElasticCloud.positional_index import get_positional_index

from upload.ElasticCloud import main

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
            result_from_elastic_search = get_positional_index()
            pos_index = result_from_elastic_search['_source']['positional_index']
    
            print(pos_index, '=res')

            result = return_docs(pos_index, search_query)

            document_ids = list(result.keys())
            print(document_ids, '= document ids')

            result_from_es_main = main.get_multiple_documents(document_ids)
            print(result_from_es_main, '= multiple docs response')

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
        positional_index = get_positional_index()
        pos_index = positional_index['hits']['hits'][0]['_source']['positional_index']
        print(pos_index, '=res')

        result = return_docs(pos_index, search_query)
        return JsonResponse({
            "data": [result]
        })
