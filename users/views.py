# -*- coding: utf-8 -*-
from django.views.generic import DetailView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegistrationForm


# Create your views here.
class UserDetails(DetailView):
    model = User
    template_name = 'users/user_detail.html'

    def get_object(self, queryset=None):
        return self.request.user


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
                  context={'form': form, 'title': 'Войти'})


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
           context={'form': form, 'title': 'Зарегистрироваться'})
