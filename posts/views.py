# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.views.generic import ListView, CreateView
from .models import Post


# Create your views here.
class PostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'


class PostCreateView(CreateView):
    model = Post
    template_name = 'posts/post_create.html'
    fields = ['title', 'content', 'blog']
    success_url = '/posts/'

    def get_context_data(self, **kwargs):
        context = super(PostCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Опубликовать'
        return context
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form)