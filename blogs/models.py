# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.
class Blog(models.Model):
    name = models.CharField('Наименование', max_length=50)
    description = models.TextField('Описание', max_length=255)