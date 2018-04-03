from django.shortcuts import render
from django.http import HttpResponse
import datetime

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

# def login(request):
#     context = {'Name': 'Omkar Pathak'}
#     return render(request, 'login.html', context)

def homepage(request):
    # context = {'Name': 'Omkar Pathak'}
    return render(request, 'homepage.html')
