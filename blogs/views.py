from django.core.paginator import Paginator
from django.db.models import Q, Prefetch
from django.http import HttpResponseNotFound
from django.shortcuts import reverse, redirect, get_object_or_404
from django.views.generic import ListView, CreateView
from posts.models import Post
from .models import Blog, Subscription
from generic.mixins import SearchMixin


class BlogsView(SearchMixin, ListView):
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

    def get_queryset(self):
        if self.request.user.is_authenticated():
            subscriptions = Subscription.objects.filter(user=self.request.user)
            blog = Blog.objects.all().prefetch_related(Prefetch('subscription_set', queryset=subscriptions))
            return blog
        else:
            return super(BlogsView, self).get_queryset()

    def post(self, request, *args, **kwargs):
        subscription = Subscription.objects.filter(blog_id=request.POST.get('blog'),
                                                   user=request.user)
        if not subscription:
            sub = Subscription(blog_id=request.POST.get('blog'),
                               user=request.user)
            sub.save()
        else:
            subscription.delete()
        return redirect(self.request.get_full_path())


class BlogCreateView(SearchMixin, CreateView):
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


class BlogPostsView(SearchMixin, ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts_list'
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        self.blog = get_object_or_404(Blog, unique_name=self.kwargs.get('blogname'))
        self.page = int(request.GET.get('page', 1))
        return super(BlogPostsView, self).get(request, *args, *kwargs)

    def get_queryset(self):
        return Post.objects.filter(blog=self.blog).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super(BlogPostsView, self).get_context_data(**kwargs)
        p = Paginator(self.get_queryset(), self.paginate_by)
        start = self.page - 2 if self.page - 2 > 0 else 1
        end = start + 5 if start + 5 <= p.num_pages else p.num_pages + 1
        start = end - 5 if end - 5 > 0 else 1
        context['custom_page_range'] = range(start, end)
        context['paginate_by'] = self.paginate_by
        context['model'] = reverse('blogs:posts', kwargs={'blogname': self.kwargs.get('blogname')})
        return context

