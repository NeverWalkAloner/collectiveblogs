from django.conf.urls import url
from .views import UserView, UserListView, user_edit, UserPostsView

urlpatterns = [
    url(r'^(?P<username>[\w.@-]+)/$', UserView.as_view(), name='detail'),
    url(r'^(?P<username>[\w.@-]+)/edit$', user_edit, name='edit'),
    url(r'^(?P<username>[\w.@-]+)/posts$', UserPostsView.as_view(), name='posts'),
    url(r'^$', UserListView.as_view(), name='list'),
]