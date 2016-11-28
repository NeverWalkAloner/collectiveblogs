# -*- coding: utf-8 -*-
from django.conf import settings
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
                               default='avatars/default.jpg',
                               null=True,
                               blank=True)

    def __str__(self):
        return self.user.username

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:
            this_record = Profile.objects.get(pk=self.id)
            if this_record.avatar != self.avatar and this_record.avatar.url != 'avatars/default.jpg':
                this_record.avatar.delete(save=False)
        except:
            pass
        super(Profile, self).save(force_insert=False, force_update=False, using=None,
             update_fields=None)

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return settings.MEDIA_URL + 'avatars/default.jpg'


class KarmaVotes(models.Model):
    vote_for = models.ForeignKey(Profile, verbose_name='За кого голосовали')
    vote_from = models.ForeignKey(User, verbose_name='Кто голосовал')
    vote_result = models.IntegerField(verbose_name='Результат голосования')
