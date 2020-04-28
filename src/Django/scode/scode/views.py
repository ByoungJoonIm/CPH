from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.generic.edit import FormView

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy

from scode.forms import LoginForm

from django.contrib.auth.models import User, Group
from django.contrib.auth.views import LoginView, LogoutView

#--- Homepage View
class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kargs):
        if not request.user.is_anonymous :
            student_group_id = Group.objects.filter(name='student').get().id
            professor_group_id = Group.objects.filter(name='professor').get().id
            
            user_group_id = request.user.groups.get().id
            
            if user_group_id == professor_group_id:
                request.session['isProfessor'] = True
                return redirect(reverse_lazy('judge:professor_subject_list'))
            else:
                request.session['isProfessor'] = False
                return redirect(reverse_lazy('judge:student_subject_list'))

class LoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = LoginForm
    redirect_field_name = 'home.html'

class LogoutView(LogoutView):
    template_name = 'home.html'
