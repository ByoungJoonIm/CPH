from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.generic.edit import FormView

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy

from scode.forms import LoginForm

from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView

#--- Homepage View
class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kargs):
        if request.user is not None:
            user_name_len = len(request.user.get_username())
            if user_name_len == 5:
                return redirect(reverse_lazy('judge:professor'))
            if user_name_len == 8:
                return redirect(reverse_lazy('judge:student'))
        return render(request, self.template_name)


class LoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = LoginForm
    redirect_field_name = 'home.html'

class LogoutView(LogoutView):
    template_name = 'home.html'
