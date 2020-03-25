from django.conf.urls import url
from django.contrib import admin

from judge.views import *

urlpatterns = [
    # example : /mainPage
    url(r'^mainPage$', UserMainLV.as_view(), name='common_subject_list'),
    
    # example : /assignment
    url(r'^assignment/(?P<subject_title>[a-zA-Z0-9]+)_(?P<classes>[0-9][0-9])/$', AssignmentLV.as_view(), name='common_assignment_list'),
]
