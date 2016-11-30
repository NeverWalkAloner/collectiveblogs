from django.contrib import admin
from .models import Blog, Subscription


# Register your models here.
admin.site.register(Blog)
admin.site.register(Subscription)