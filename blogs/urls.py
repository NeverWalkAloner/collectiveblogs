from django.conf.urls import url
from .views import BlogsView, BlogCreateView


urlpatterns = [
    url(r'^$', BlogsView.as_view(), name='list'),
    url(r'^create/$', BlogCreateView.as_view(), name='create'),
]