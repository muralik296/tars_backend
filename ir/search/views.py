# Create your views here.
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import json

from upload.ElasticCloud.elasticCloud import client

index_name = 'ir_project'


@csrf_exempt
def searchHandler(request):
    if (request.method == 'GET'):
        return JsonResponse({
            'msg': 'search'
        })
    elif (request.method == 'POST'):
        requestBody = json.loads(request.body)
        searchQuery = requestBody['query']

        # make search query smallcase
        # searchQuery = searchQuery.lower()

        result = client.search(
            index=index_name,
            query={
                'match_phrase': {'content': {
                    'query': searchQuery
                }}
            })

        # use the search query to perform the phrase query search
        return JsonResponse({
            'data': result['hits']['hits']
        })


def getDocumentById(request, documentId):
    print(documentId, '=documentid')
    result = client.search(
        index=index_name,
        query={
            'match': {'documentid': {
                'query': documentId
            }}
        })
    
    return JsonResponse({
        'data': result['hits']['hits']
    })
