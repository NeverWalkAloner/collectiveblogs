# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError('Неверный логин или пароль!')
        if not user.check_password(password):
            raise forms.ValidationError('Неверный пароль')
        if not user.is_active:
            raise forms.ValidationError('Пользователь заблокирован')
        return super(LoginForm, self).clean()


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    email = forms.EmailField(label='Email')
    email2 = forms.EmailField(label='Подтвердите Email')

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'email2',
            'password'
        ]

    def clean_email2(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email != email2:
            raise forms.ValidationError('Адреса email не совпадают!')
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError('пользователь с таким email уже зарегистрирован!')
        return email


class UserSettingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class ProfileSettingForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['about',]