from django.shortcuts import render
from django.views.generic import ListView


def blog_list(request):
    return render(request, template_name='blogs/blog_list.html')