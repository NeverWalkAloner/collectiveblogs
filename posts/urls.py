from django.conf.urls import url
from .views import (PostListView,
                    PostCreateView,
                    PostDetailView,
                    BestPostsView,
                    SubscriptionView)

urlpatterns = [
    url(r'^$', PostListView.as_view(), name='list'),
    url(r'^best/$', BestPostsView.as_view(), name='best'),
    url(r'^subscription/$', SubscriptionView.as_view(), name='subscription'),
    url(r'^create/$', PostCreateView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', PostDetailView.as_view(), name='detail'),
]