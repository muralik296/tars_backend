from django.urls import path
from . import views

urlpatterns = [
    path('', views.searchHandler, name='search'),
    path('getDocument/<str:documentId>/', views.getDocumentById , name='getDocumentById'),
    path('getDocuments',views.get_posting_list_for_phrase,name='getDocuments')
]