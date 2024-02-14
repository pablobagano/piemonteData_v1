from django.urls import path
from piemonteStructure.views import index, CustomLoginView, profile
urlpatterns = [
    path('', index, name='index'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile', profile, name='profile')
]
