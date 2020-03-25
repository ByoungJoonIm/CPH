from django.conf.urls import url
from django.contrib import admin

from judge.views import *

urlpatterns = [
    # example : /professor
    url(r'^professor$', ProfessorMainLV.as_view(), name='professor'),
    
    # example : /professor/python_01
    url(r'^professor/(?P<subject_title>[a-zA-Z0-9]+)_(?P<classes>[0-9][0-9])/$', ProfessorAssignmentLV.as_view(), name='assignment'),
]
