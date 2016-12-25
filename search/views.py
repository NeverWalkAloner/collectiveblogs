from django.core.paginator import Paginator
from django.shortcuts import render, reverse
from django.db.models import Q
from django.views.generic import ListView
from posts.models import Post


# Create your views here.
class SearchView(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts_list'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.q = request.GET.get('q')
        self.page = int(request.GET.get('page', 1))
        return super(SearchView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return Post.objects.filter(Q(title__icontains=self.q)|Q(content__icontains=self.q))

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        p = Paginator(self.get_queryset(), self.paginate_by)
        start = self.page - 2 if self.page - 2 > 0 else 1
        end = start + 5 if start + 5 <= p.num_pages else p.num_pages + 1
        start = end - 5 if end - 5 > 0 else 1
        context['custom_page_range'] = range(start, end)
        context['paginate_by'] = self.paginate_by
        context['model'] = reverse('search:main') + '?q=' + self.q
        return context