# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)

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
