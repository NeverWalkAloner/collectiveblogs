from django.conf.urls import url
from .views import mainpage

urlpatterns = [
    url(r'^$', mainpage, name='main'),
]