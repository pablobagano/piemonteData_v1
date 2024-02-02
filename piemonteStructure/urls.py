from django.urls import path
from piemonteStructure.views import index, UserDataView
urlpatterns = [
    path('', index, name='index'),
    path('userdata/', UserDataView, name= 'userdata')
]
