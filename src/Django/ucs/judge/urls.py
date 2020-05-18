from django.conf.urls import url
from django.contrib import admin

from judge.views import *

urlpatterns = [
    # example : /professor/subject_list
    url(r'^professor/subject_list$', ProfessorSubjectLV.as_view(), name='professor_subject_list'),
    
    # example : /professor/subject_add
    url(r'^professor/subject_add$', ProfessorSubjectAddView.as_view(), name='professor_subject_add'),

    # example : /professor/hided_subject
    url(r'^professor/hided_subject$', ProfessorSubjectHidedLV.as_view(), name='professor_hided_subject'),

    # example : /professor/assignment_list
    url(r'^professor/assignment_list$', ProfessorAssignmentLV.as_view(), name='professor_assignment_list'),

    # example : /professor/assignment_result
    url(r'^professor/assignment_result$', ProfessorAssignmentResultLV.as_view(), name='professor_assignment_result'),

    # example : /professor/assignment_add
    url(r'^professor/assignment_add$', ProfessorAssignmentAddView.as_view(), name='professor_assignment_add'),

    # example : /professor/assignment_id/update
    url(r'^professor/update$', ProfessorAssignmentUpdateView.as_view(), name='professor_assignment_update'),

    # example : /professor/assignment_student_code
    url(r'^professor/assgnment_student_code$', ProfessorAssignmentStudentCodeView.as_view(), name='professor_assignment_student_code'),

    # example : /professor/subject_management
    url(r'^professor/subject_management$', ProfessorSubjectManagementView.as_view(), name='professor_subject_management'),

    # example : /student/subject_list
    url(r'^student/subject_list$', StudentSubjectLV.as_view(), name='student_subject_list'),

    # example : /student/subject_add
    url(r'^student/subject_add$', StudentSubjectAddView.as_view(), name='student_subject_add'),

    # example : /student/assignment_list
    url(r'^student/assignment_list$', StudentAssignmentLV.as_view(), name='student_assignment_list'),

    # example : /student/assignment_id
    url(r'^student/(?P<assignment_id>[0-9]+)$', StudentAssignment.as_view(), name='student_assignment'),
    
]
