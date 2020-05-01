from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.generic.edit import FormView

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy

from ucs.forms import LoginForm

from django.contrib.auth.models import User, Group
from django.contrib.auth.views import LoginView, LogoutView

#--- Homepage View
class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kargs):
        cur_user = request.user
        if cur_user.is_anonymous :
            return render(request, self.template_name)
        
        if cur_user.has_perm('judge.professor'):
            return redirect(reverse_lazy('judge:professor_subject_list'))
        if cur_user.has_perm('judge.student'):
            return redirect(reverse_lazy('judge:student_subject_list'))
        
        return render(request, self.template_name)  #This will not be occured

class LoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = LoginForm
    redirect_field_name = 'home.html'

class LogoutView(LogoutView):
    template_name = 'home.html'
