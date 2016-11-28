# -*- coding: utf-8 -*-
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


unique_validator = RegexValidator(r'[\w-]+', 'Допустимы только символы латинского алфавита и знак -')


class Blog(models.Model):
    name = models.CharField('Наименование', max_length=50)
    description = models.TextField('Описание', max_length=255)
    unique_name = models.CharField('Уникальные идентификатор',
                                   max_length=50,
                                   unique=True,
                                   blank=False,
                                   validators=[unique_validator])


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)