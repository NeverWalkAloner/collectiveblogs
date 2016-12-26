"""collectiveblogs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib.auth.views import logout
from django.contrib import admin
from users.views import user_login, user_registration

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', user_login, name='login'),
    url(r'^register/$', user_registration, name='registration'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^', include('posts.urls', namespace='main')),
    url('^users/', include('users.urls', namespace='users')),
    url('^blogs/', include('blogs.urls', namespace='blogs')),
    url(r'^posts/', include('posts.urls', namespace='posts')),
    url(r'^search/', include('search.urls', namespace='search')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)