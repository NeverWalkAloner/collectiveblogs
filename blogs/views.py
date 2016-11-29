from django.core.paginator import Paginator
from django.shortcuts import reverse
from django.views.generic import ListView, CreateView
from .models import Blog


class BlogsView(ListView):
    model = Blog
    template_name = 'blogs/blog_list.html'
    paginate_by = 5
    context_object_name = 'blogs_list'

    def get(self, request, *args, **kwargs):
        self.page = int(request.GET.get('page', 1))
        return super(BlogsView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BlogsView, self).get_context_data(**kwargs)
        context['model'] = reverse('blogs:list')
        context['paginate_by'] = self.paginate_by
        p = Paginator(self.get_queryset(), self.paginate_by)
        start = self.page - 2 if self.page - 2 > 0 else 1
        end = start + 5 if start + 5 <= p.num_pages else p.num_pages + 1
        start = end - 5 if end - 5 > 0 else 1
        context['custom_page_range'] = range(start, end)
        return context


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
        form.instance.owner = self.request.user
        return super(BlogCreateView, self).form_valid(form)
