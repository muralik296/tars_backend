from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# home page
def home(request):
    return JsonResponse({
        "msg": "Home"
    })
