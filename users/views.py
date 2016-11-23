# -*- coding: utf-8 -*-
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegistrationForm, UserSettingForm, ProfileSettingForm
from .models import Profile


# Create your views here.
class UserDetails(DetailView):
    model = User
    template_name = 'users/user_detail.html'

    def get_object(self, queryset=None):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return user


class KarmaVote(UpdateView):
    model = Profile
    template_name = 'users/user_detail.html'
    fields = []

    def get_object(self, queryset=None):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return user

    def post(self, request, *args, **kwargs):
        print('ggfghfhghgf')
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        self.profile = get_object_or_404(Profile, user=user)
        self.profile.karma += int(request.POST.get('karma', 0))
        self.profile.save()
        return redirect('users:detail', username=self.kwargs.get('username'))


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
        profile_form = ProfileSettingForm(request.POST or None, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user.first_name = user_form.cleaned_data.get('first_name')
            user.last_name = user_form.cleaned_data.get('last_name')
            profile.about = profile_form.cleaned_data.get('about')
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
