# -* coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField('О себе', blank=True)
    karma = models.PositiveIntegerField(verbose_name='карма', default=0)
