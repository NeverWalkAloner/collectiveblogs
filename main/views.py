from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def mainpage(request):
    if request.user.is_authenticated():
        return HttpResponse('Welcome to the main page, {}!'.format(request.user))
    else:
        return HttpResponse("Dr. Livingstone, I presume")
