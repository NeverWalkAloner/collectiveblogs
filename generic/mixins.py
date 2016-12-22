from django.http import HttpResponseRedirect
from django.shortcuts import reverse


class SearchMixin(object):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q')
        if request.GET.get('q'):
            return HttpResponseRedirect(reverse('search:main') + '?q=' + q)
        return super(SearchMixin, self).get(request, *args, **kwargs)