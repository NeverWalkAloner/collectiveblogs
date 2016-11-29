from django.shortcuts import render, reverse
from django.views.generic import ListView, CreateView
from .models import Blog
from .forms import BlogForm


class BlogsView(ListView):
    model = Blog
    template_name = 'blogs/blog_list.html'
    paginate_by = 5
    context_object_name = 'blogs_list'

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('p')
        return super(BlogsView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(BlogsView, self).get_context_data(**kwargs)


class BlogCreateView(CreateView):
    model = Blog
    fields = ['name', 'description', 'unique_name']
    template_name = 'blogs/blog_edit.html'
    success_url = '/blogs/'

    def get_context_data(self, **kwargs):
        context = super(BlogCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Создать блог'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(BlogCreateView, self).form_valid(form)
