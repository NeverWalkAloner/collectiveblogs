# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.views.generic import ListView, CreateView
from .models import Post


# Create your views here.
class PostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts_list'
    paginate_by = 1

    def get(self, request, *args, **kwargs):
        self.page = int(request.GET.get('page', 1))
        return super(PostListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        p = Paginator(self.get_queryset(), self.paginate_by)
        start = self.page - 2 if self.page - 2 > 0 else 1
        end = start + 5 if start + 5 <= p.num_pages else p.num_pages + 1
        start = end - 5 if end - 5 > 0 else 1
        context['custom_page_range'] = range(start, end)
        context['paginate_by'] = self.paginate_by
        context['model'] = reverse('posts:list')
        return context


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