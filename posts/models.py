from django.db import models
from django.contrib.auth.models import User
from blogs.models import Blog
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from markdown_deux import markdown
from taggit.managers import TaggableManager


# Create your models here.
class Post(models.Model):
    title = models.CharField('Публикация', max_length=255)
    content = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name='Блог')
    rating = models.IntegerField('Рейтинг', default=0)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    tags = TaggableManager(blank=True, verbose_name='Теги')

    def __str__(self):
        return self.title

    def get_markdown(self):
        return mark_safe(markdown(self.content))

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'pk': self.id})


class PostVotes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    result = models.IntegerField(verbose_name='Результат голосования', default=0)