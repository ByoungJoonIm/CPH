from django.conf.urls import url
from django.contrib import admin

from judge.views import *

urlpatterns = [
    # example : /mainPage
    url(r'^mainPage$', UserMainLV.as_view(), name='common_subject_list'),
    
    # example : /assignment/Algorithm_01
    url(r'^assignment/(?P<subject_title>[a-zA-Z0-9]+)_(?P<classes>[0-9][0-9])$', AssignmentLV.as_view(), name='common_assignment_list'),

    # example : /professor/assignment_add
    url(r'^professor/assignment_add$', ProfessorAddView.as_view(), name='professor_assignment_add'),

    # example : /professor/assignment_id/update
    url(r'^professor/update$', ProfessorUpdateView.as_view(), name='professor_assignment_update'),

    # example : /student/assignment_id
    url(r'^student/(?P<assignment_id>[0-9]+)$', StudentAssignment.as_view(), name='student_assignment'),
]
