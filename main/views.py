from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def mainpage(request):
    if request.user.is_authenticated():
        cxt = {'cxt': 'Welcome to the main page, {}!'.format(request.user)}
    else:
        cxt = {'cxt': 'Dr. Livingstone, I presume?'}
    return render(request, context=cxt, template_name='main/main.html')
