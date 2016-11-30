# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


unique_validator = RegexValidator(r'^[a-zA-Z-]+$', 'Допустимы только символы латинского алфавита и знак -')


class Blog(models.Model):
    name = models.CharField('Наименование', max_length=50)
    description = models.TextField('Описание', max_length=255)
    unique_name = models.CharField('Уникальные идентификатор',
                                   max_length=50,
                                   unique=True,
                                   blank=False,
                                   validators=[unique_validator,])
    owner = models.ForeignKey(User,
                              verbose_name='Создатель блога',
                              blank=True,
                              null=True)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username