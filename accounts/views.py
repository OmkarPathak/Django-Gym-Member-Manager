from django.shortcuts import render
from django.http import HttpResponse
import datetime

def homepage(request):
    return render(request, 'homepage.html')

def homepage_after_login(request):
    return render(request, 'homepage_after_login.html')
