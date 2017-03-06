# -*- coding:utf-8 -*-
import datetime
from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.utils import timezone
from blogs.models import Subscription
from .forms import PostForm
from .models import Post, PostVotes
from comments.forms import CommentForm
from comments.models import Comment
from generic.mixins import SearchMixin


# Create your views here.
class PostListView(SearchMixin, ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts_list'
    paginate_by = 10
    ordering = ['-pub_date',]

    def get(self, request, *args, **kwargs):
        self.page = int(request.GET.get('page', 1))
        self.tag = request.GET.get('tag')
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

    def get_queryset(self):
        posts = super(PostListView, self).get_queryset()
        if self.tag:
            posts = posts.filter(tags__name=self.tag)
        return posts


class PostCreateView(SearchMixin, CreateView):
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


class PostDetailView(SearchMixin, UpdateView):
    model = Post
    template_name = 'posts/post_details.html'
    fields = []

    def get(self, request, *args, **kwargs):
        return super(PostDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            initial_data = {'content_type': self.object.get_content_type,
                            'obj_id': self.object.id}
            comment_form = CommentForm(initial=initial_data)
            voted = PostVotes.objects.filter(post=self.object, voter=self.request.user).exists()
            vote = PostVotes.objects.filter(post=self.object, voter=self.request.user).first()
            context['voted'] = voted
            context['comment_form'] = comment_form
            if voted:
                if vote.result > 0:
                    context['enable'] = 'up'
                else:
                    context['enable'] = 'down'
        return context

    def post(self, request, *args, **kwargs):
        super(PostDetailView, self).post(request, *args, **kwargs)
        comment_form = CommentForm(request.POST)
        if request.user.is_authenticated():
            voted = PostVotes.objects.filter(post=self.object, voter=self.request.user).exists()
            if not voted and self.request.POST.get('vote'):
                self.object.rating += int(self.request.POST.get('vote'))
                self.object.save()
                post_vote = PostVotes.objects.create(post=self.object, voter=self.request.user)
                post_vote.save()
                return redirect('posts:detail', pk=kwargs.get('pk'))
            if comment_form.is_valid():
                c_type = comment_form.cleaned_data.get('content_type')
                content_type = ContentType.objects.get(model=c_type)
                obj_id = int(comment_form.cleaned_data.get('obj_id'))
                content = comment_form.cleaned_data.get('content')
                Comment.objects.create(user=request.user,
                                       content_type=content_type,
                                       object_id=obj_id,
                                       content=content)
            return redirect('posts:detail', pk=kwargs.get('pk'))


class BestPostsView(SearchMixin, ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts_list'
    paginate_by = 10

    def get_queryset(self):
        start = timezone.now() -datetime.timedelta(days=1)
        return Post.objects.filter(pub_date__gt=start).order_by('-rating')[:3]


class SubscriptionView(SearchMixin, ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts_list'
    paginate_by = 10

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
