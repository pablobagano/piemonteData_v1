from django.urls import path
from piemonteStructure.views import index
urlpatterns = [
    path('', index, name='index')
]
