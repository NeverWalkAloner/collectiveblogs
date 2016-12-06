from django.conf.urls import url
from .views import PostListView, PostCreateView, PostDetailView

urlpatterns = [
    url(r'^$', PostListView.as_view(), name='list'),
    url(r'^create/$', PostCreateView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', PostDetailView.as_view(), name='detail'),
]