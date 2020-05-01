from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin

class ProfessorMixin(PermissionRequiredMixin, LoginRequiredMixin):
    permission_required = 'judge.professor'
    
class StudentMixin(PermissionRequiredMixin, LoginRequiredMixin):
    permission_required = 'judge.student'