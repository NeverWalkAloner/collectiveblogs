# -* coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


def upload_location(instance, filename):
    return 'avatars/{}/{}'.format(instance.id, filename)


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField('О себе', blank=True)
    karma = models.PositiveIntegerField(verbose_name='карма', default=0)
    avatar = models.ImageField(verbose_name='Аватар',
                               upload_to=upload_location,
                               null=True,
                               blank=True)

    def __str__(self):
        return self.user.username


class KarmaVotes(models.Model):
    vote_for = models.ForeignKey(Profile, verbose_name='За кого голосовали')
    vote_from = models.ForeignKey(User, verbose_name='Кто голосовал')
    vote_result = models.IntegerField(verbose_name='Результат голосования')
