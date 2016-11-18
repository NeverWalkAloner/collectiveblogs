from django.views.generic import DetailView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


# Create your views here.
class UserDetails(DetailView):
    model = User
    template_name = 'users/user_detail.html'

    def get_object(self, queryset=None):
        return self.request.user