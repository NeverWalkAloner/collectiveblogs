# -*- coding:utf-8 -*-
import datetime
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.utils import timezone
from blogs.models import Subscription
from .forms import PostForm
from .models import Post, PostVotes


# Create your views here.
class PostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts_list'
    paginate_by = 3
    ordering = ['-pub_date',]

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
    form_class = PostForm
    success_url = '/posts/'

    def get_context_data(self, **kwargs):
        context = super(PostCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Опубликовать'
        return context
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form)


class PostDetailView(UpdateView):
    model = Post
    template_name = 'posts/post_details.html'
    fields = []

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            voted = PostVotes.objects.filter(post=self.object, voter=self.request.user).exists()
            vote = PostVotes.objects.filter(post=self.object, voter=self.request.user).first()
            context['voted'] = voted
            if voted:
                if vote.result > 0:
                    context['enable'] = 'up'
                else:
                    context['enable'] = 'down'
        return context

    def post(self, request, *args, **kwargs):
        super(PostDetailView, self).post(request, *args, **kwargs)
        if request.user.is_authenticated():
            voted = PostVotes.objects.filter(post=self.object, voter=self.request.user).exists()
            if not voted:
                self.object.rating += int(self.request.POST.get('vote'))
                self.object.save()
                post_vote = PostVotes.objects.create(post=self.object, voter=self.request.user)
                post_vote.save()
                return redirect('posts:detail', pk=kwargs.get('pk'))


class BestPostsView(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts_list'
    paginate_by = 3

    def get_queryset(self):
        start = timezone.now() -datetime.timedelta(days=1)
        return Post.objects.filter(pub_date__gt=start).order_by('-rating')[:3]


class SubscriptionView(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts_list'
    paginate_by = 3

    def get_queryset(self):
        subscriptions = Subscription.objects.filter(user__id=self.request.user.id).values('blog')
        posts = Post.objects.filter(blog__in=subscriptions)
        print(posts)
        return posts

    def get(self, request, *args, **kwargs):
        self.page = int(request.GET.get('page', 1))
        return super(SubscriptionView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SubscriptionView, self).get_context_data(**kwargs)
        p = Paginator(self.get_queryset(), self.paginate_by)
        start = self.page - 2 if self.page - 2 > 0 else 1
        end = start + 5 if start + 5 <= p.num_pages else p.num_pages + 1
        start = end - 5 if end - 5 > 0 else 1
        context['custom_page_range'] = range(start, end)
        context['paginate_by'] = self.paginate_by
        context['model'] = reverse('posts:subscription')
        return context
