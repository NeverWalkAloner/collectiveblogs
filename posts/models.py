from django.db import models
from blogs.models import Blog
from users.models import Profile


# Create your models here.
class Post(models.Model):
    title = models.CharField('Публикация', max_length=255)
    content = models.TextField('Текст')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField('Рейтинг')