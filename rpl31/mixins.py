from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse


class UserMixin(object):
    def dispatch(self, request, *args, **kwargs):
        user = self.request.session.get('username')
        if user:
            return super(UserMixin, self).dispatch(request, *args, **kwargs)
        else:
            logout(self.request)
        return HttpResponseRedirect(reverse('home'))
