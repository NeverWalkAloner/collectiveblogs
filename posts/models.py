from django.db import models
from django.contrib.auth.models import User
from blogs.models import Blog
from django.utils import timezone
from markdown_deux import markdown


# Create your models here.
class Post(models.Model):
    title = models.CharField('Публикация', max_length=255)
    content = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name='Блог')
    rating = models.PositiveIntegerField('Рейтинг', default=0)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.title

    def get_markdown(self):
        return markdown(self.content)