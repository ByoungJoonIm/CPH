from django.conf.urls import url
from django.contrib import admin

from judge.views import *

urlpatterns = [
    # example : /professor/subject_list
    url(r'^professor/subject_list$', ProfessorSubjectLV.as_view(), name='professor_subject_list'),
    
    # example : /professor/subject_add
    url(r'^professor/subject_add$', ProfessorAddSubjectView.as_view(), name='professor_subject_add'),

    # example : /professor/hided_subject
    url(r'^professor/hided_subject$', ProfessorHidedSubjectLV.as_view(), name='professor_hided_subject'),

    # example : /professor/assignment_list
    url(r'^professor/assignment_list$', ProfessorAssignmentLV.as_view(), name='professor_assignment_list'),

    # example : /professor/assignment_add
    url(r'^professor/assignment_add$', ProfessorAddAssignmentView.as_view(), name='professor_assignment_add'),

    # example : /professor/assignment_id/update
    url(r'^professor/update$', ProfessorUpdateView.as_view(), name='professor_assignment_update'),

    # example : /professor/subject_management
    url(r'^professor/subject_management$', ProfessorSubjectManagement.as_view(), name='professor_subject_management'),

    # example : /student/subject_list
    url(r'^student/subject_list$', StudentSubjectLV.as_view(), name='student_subject_list'),

    # example : /student/assignment_list
    url(r'^student/assignment_list$', StudentAssignmentLV.as_view(), name='student_assignment_list'),

    # example : /student/assignment_id
    url(r'^student/(?P<assignment_id>[0-9]+)$', StudentAssignment.as_view(), name='student_assignment'),
    
]
