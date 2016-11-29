# -*- coding: utf-8 -*-
from django.views.generic import DetailView, ListView
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegistrationForm, UserSettingForm, ProfileSettingForm
from .models import Profile, KarmaVotes


def karma_valid(user, current_user, karma_value, votes):
    if user == current_user:
        return False
    if votes:
        if votes[0].vote_result > 0 and karma_value > 0:
            return False
        if votes[0].vote_result < 0 and karma_value < 0:
            return False
    return True


class UserListView(ListView):
    model = Profile
    paginate_by = 3
    template_name = 'users/user_list.html'
    context_object_name = 'users_list'
    ordering = ['-karma',]

    def get(self, request, *args, **kwargs):
        self.page = int(request.GET.get('page', 1))
        return super(UserListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        p = Paginator(self.get_queryset(), self.paginate_by)
        start = self.page - 2 if self.page - 2 > 0 else 1
        end = start + 5 if start + 5 <= p.num_pages else p.num_pages + 1
        start = end - 5 if end - 5 > 0 else 1
        context['custom_page_range'] = range(start, end)
        context['paginate_by'] = self.paginate_by
        context['model'] = reverse('users:list')
        return context


class UserView(UpdateView):
    model = Profile
    template_name = 'users/user_detail.html'
    fields = []

    def get_object(self, queryset=None):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return user

    def post(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, username=self.kwargs.get('username'))
        self.profile = get_object_or_404(Profile, user=self.user)
        self.votes = KarmaVotes.objects.filter(vote_for=self.profile, vote_from=request.user)
        if not karma_valid(self.user,
                           request.user,
                           int(request.POST.get('karma', 0)),
                           self.votes):
            return redirect('users:detail', username=self.kwargs.get('username'))
        if self.votes:
            self.profile.karma -= self.votes[0].vote_result
            if self.profile.karma == 0 and int(request.POST.get('karma', 0)) < 0:
                self.votes[0].vote_result = 0
            else:
                self.votes[0].vote_result = int(request.POST.get('karma', 0))
            self.votes[0].save()
        else:
            vote = KarmaVotes.objects.create(vote_for=self.profile,
                                            vote_from=request.user,
                                            vote_result=int(request.POST.get('karma', 0)))
            vote.save()
        self.profile.karma += int(request.POST.get('karma', 0))
        if self.profile.karma < 0:
            self.profile.karma = 0
        self.profile.save()
        return redirect('users:detail', username=self.kwargs.get('username'))

    def get(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, username=self.kwargs.get('username'))
        self.profile = get_object_or_404(Profile, user=self.user)
        self.votes = KarmaVotes.objects.filter(vote_for=self.profile, vote_from=request.user)
        return super(UserView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)
        context['enable'] = ''
        if self.votes:
            if self.votes[0].vote_result > 0:
                context['enable'] = 'down'
            else:
                context['enable'] = 'up'
        return context


def user_login(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('main:main')
    return render(request,
                  template_name='form.html',
                  context={'forms': [form, ], 'title': 'Войти'})


def user_registration(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        authenticate(username=user.username, password=password)
        login(request, user)
        return redirect('main:main')
    return render(request,
           template_name='form.html',
           context={'forms': [form, ], 'title': 'Зарегистрироваться'})


def user_edit(request, username):
    user = get_object_or_404(User, username=username)
    if request.user == user:
        profile = get_object_or_404(Profile, user=user)
        user_form = UserSettingForm(request.POST or None, instance=user)
        profile_form = ProfileSettingForm(request.POST or None,
                                          request.FILES or None,
                                          instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user.first_name = user_form.cleaned_data.get('first_name')
            user.last_name = user_form.cleaned_data.get('last_name')
            profile.about = profile_form.cleaned_data.get('about')
            if profile_form.cleaned_data.get('avatar'):
                profile.avatar = profile_form.cleaned_data.get('avatar')
            user.save()
            profile.save()
            return redirect('users:detail', username=username)
        return render(request,
                      template_name='users/user_edit.html',
                      context={'forms': [user_form, profile_form],
                               'title': 'Редактировать',
                               'user': user})
    else:
        raise Http404()
