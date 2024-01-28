from django.shortcuts import render, HttpResponse
import datetime

# Create your views here.
def index(request):
    now = datetime.datetime.now().date()
    html = f'<html><body><h1>Now it is {now}</h1></body></html>'
    return HttpResponse(html)