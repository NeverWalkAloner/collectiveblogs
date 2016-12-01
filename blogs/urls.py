from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import BlogsView, BlogCreateView


urlpatterns = [
    url(r'^$', BlogsView.as_view(), name='list'),
    url(r'^create/$', login_required(BlogCreateView.as_view()), name='create'),
]