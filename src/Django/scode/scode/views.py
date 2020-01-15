from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.generic.edit import FormView

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy

from judge.models import Professor
from judge.forms import LoginForm

from judge.judgeManager import JudgeManager
from scode.loginManager import LoginManager

from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView

#--- Homepage View
class HomeView(TemplateView, LoginManager):
    template_name = 'home.html'

    def get(self, request, *args, **kargs):
        if self.is_activate(request):
            if request.session['role'] == 'professor':
                return redirect(reverse_lazy('judge:Professor'))
            if request.session['role'] == 'student':
                return redirect(reverse_lazy('judge:Student'))
        return render(request, self.template_name)

class LoginView(FormView, LoginManager):
    template_name = 'registration/login.html'
    form_class = LoginForm

    success_url = template_name

    def get(self, request, *args, **kargs):
        return render(request, self.template_name, {'form' : self.form_class})

    def post(self, request, *args, **kargs):
        form = request.POST
        login_id = form.get('userid')
        login_password = form.get('password')

        return self.login(request, login_id, login_password)


class LogoutView(LogoutView):
    template_name = 'home.html'
