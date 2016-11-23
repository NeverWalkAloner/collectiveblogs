from django.conf.urls import url
from .views import KarmaVote, user_edit

urlpatterns = [
    url(r'^(?P<username>[\w.@-]+)/$', KarmaVote.as_view(), name='detail'),
    url(r'^(?P<username>[\w.@-]+)/edit$', user_edit, name='edit'),
]