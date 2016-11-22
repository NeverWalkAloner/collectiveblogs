from django.conf.urls import url
from .views import UserDetails, user_edit

urlpatterns = [
    url(r'^(?P<username>[\w.@-]+)/$', UserDetails.as_view(), name='detail'),
    url(r'^(?P<username>[\w.@-]+)/edit$', user_edit, name='edit'),
]