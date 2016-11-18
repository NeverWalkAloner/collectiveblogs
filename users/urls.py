from django.conf.urls import url
from .views import UserDetails

urlpatterns = [
    url(r'^(?P<username>[\w.@-]+)/$', UserDetails.as_view(), name='detail')
]