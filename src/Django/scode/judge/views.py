# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.views.generic.base import TemplateView

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from django.db import connection

from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin

from judge.models import *
from judge.forms import AssignmentForm, AssignmentUpdateForm, CodingForm


from judge.judgeManager import JudgeManager
from scode.loginManager import LoginManager

import pymysql
import os
import pathlib
import datetime
import zipfile
import time
import datetime
from django.utils import timezone


#-- Here is developing area    
# common area------------------------------------------------------------------------------------------------------------------------
class UserMainLV(LoginRequiredMixin, ListView):
    template_name = 'judge/common/common_subject_list.html'
    
    def get(self, request, *args, **kwargs):
        signup_class = Signup_class.objects.filter(user_id=self.request.user.id).values_list('subject_id')
        subject = Subject.objects.filter(pk__in = signup_class)
        
        return render(request, self.template_name, { 'subject' : subject })
    
class AssignmentLV(LoginRequiredMixin, ListView):
    template_name = 'judge/common/common_assignment_list.html'
    paginate_by = 10
    
    def post(self, request, *args, **kwargs):
        subject_id = request.POST.get('subject_id')
        request.session['subject_id'] = subject_id
        
        return self.get(request, args, kwargs)

    @classmethod
    def get(self, request, *args, **kwargs):
        if('subject_id' not in request.session):
            return redirect(reverse_lazy('judge:common_subject_list'))
        
        subject_id = request.session.get('subject_id')
        assignment = Assignment.objects.filter(subject_id = subject_id)
        subject = Subject.objects.get(id = subject_id)
        
        return render(request, self.template_name, { 'assignment' : assignment, 'subject' : subject })
    
# professor area------------------------------------------------------------------------------------------------------------------------
class ProfessorAddView(LoginRequiredMixin, FormView):
    template_name = 'judge/professor/professor_assignment_add.html'
    form_class = AssignmentForm

    def post(self, request, *args, **kwargs):
        subject = Subject.objects.get(id = request.session.get('subject_id'))
            
        base_dir_path = self.get_base_dir_path(self.request)
        self.construct_dir(base_dir_path)
        self.upload_files(self.request, base_dir_path)
        self.generate_problem_file(self.request, base_dir_path)
            
        return AssignmentLV.get(request, args, kwargs)

    def get_base_dir_path(self, request):
        subject = Subject.objects.get(id = request.session.get('subject_id'))
            
        #/user/student_codes/2019_1/00001/Algorithm_01/temp
        base_dir_path = os.path.expanduser('~')
        base_dir_path = os.path.join(base_dir_path, "student_codes")
        base_dir_path = os.path.join(base_dir_path, str(subject.year) + "_" + str(subject.semester))
        base_dir_path = os.path.join(base_dir_path, request.user.username)
        base_dir_path = os.path.join(base_dir_path, subject.title + "_" + subject.classes)
        return base_dir_path    

    def construct_dir(self, base_dir_path):
        if not os.path.exists(base_dir_path):
            dir_elem = ['students', 'temp', 'problems', 'settings']
            pathlib.Path(base_dir_path).mkdir(parents=True, exist_ok=True)
            for de in dir_elem:
                os.mkdir(os.path.join(base_dir_path, de))
        
    def upload_files(self, request, base_dir_path):
        origin_file_name = ['assignment_in_file', 'assignment_out_file']
        uploaded_file_name = ['in', 'out']
            
        for seq in range(0, 2):
            with open(os.path.join(os.path.join(base_dir_path, "temp"), uploaded_file_name[seq]), 'wb+') as dest:
                for chunk in request.FILES[origin_file_name[seq]].chunks():
                    dest.write(chunk)
                    
    def generate_problem_file(self, request, base_dir_path):
        sequence = str(len(Assignment.objects.filter(subject = request.session.get('subject_id'))) + 1)
        
        #when delete assignment, error will be occured. It need to fix
        for dir in ["problems", "students"]:
            os.mkdir(os.path.join(os.path.join(base_dir_path, dir), sequence))
        
        os.chdir(os.path.join(base_dir_path, 'temp'))
        
        #--- separate files
        in_file = open("in", "r")
        out_file = open("out", "r")
        cnt = 0

        zip_name = sequence + ".zip"
        myzip = zipfile.ZipFile(zip_name, "w")

        file_list = ["in", "out"]

        while True:
            in_line = in_file.readline().rstrip()
            out_line = out_file.readline().rstrip()
            if not in_line or not out_line:
                break

            cnt = cnt + 1
            
            in_file_rs_name = sequence + "." + str(cnt) + ".in"
            in_file_rs = open(in_file_rs_name, "w")
            in_file_rs.write('1\n')
            in_file_rs.write(str(in_line) + '\n')
            in_file_rs.close()

            out_file_rs_name = sequence + "." + str(cnt) + ".out"
            out_file_rs = open(out_file_rs_name, "w")
            out_file_rs.write(str(out_line) + '\n')
            out_file_rs.close()

            myzip.write(in_file_rs_name)
            myzip.write(out_file_rs_name)

            file_list.append(in_file_rs_name)
            file_list.append(out_file_rs_name)

        in_file.close()
        out_file.close()

        myzip.close()

        #--- remove files
        for f in file_list:
            os.remove(os.path.join(os.path.join(base_dir_path, "temp"), f))

        problem_path = os.path.join(os.path.join(base_dir_path, "problems"), sequence)
        #--- generate init file
        init_file_name = "init.yml"
        init_file_path = os.path.join(problem_path, init_file_name)
        init_file = open(init_file_path, "w")
        init_file.write("archive: {0}.zip\ntest_cases:".format(sequence))

        for i in range(1, cnt):
            init_file.write("\n- {" + "in: {0}.{1}.in, out: {0}.{1}.out, points: 1".format(sequence, i) + "}")

        init_file.close()
        os.rename(zip_name, os.path.join(problem_path, zip_name))
        
        #--- insert to database    
        assignment_instance = Assignment()
        assignment_instance.name = request.POST.get('assignment_name')
        assignment_instance.desc = request.POST.get('assignment_desc')
        assignment_instance.deadline = timezone.make_aware(datetime.datetime.now() + datetime.timedelta(days=int(request.POST.get('assignment_deadline'))))
        assignment_instance.max_score = cnt
        assignment_instance.subject = Subject.objects.get(id=int(request.session.get('subject_id')))
        assignment_instance.save()

        
class ProfessorUpdateView(LoginRequiredMixin, FormView):
    template_name = 'judge/professor/professor_assignment_update.html'
    form_class = AssignmentUpdateForm
        
    def get(self, request, * args, **kwargs):
        assignment_id = request.GET.get('assignment_id')
        request.session['assignment_id'] = assignment_id
        return render(request, self.template_name, {'form' : self.form_class, 'assignment' : Assignment.objects.get(id=assignment_id)})   # + current assignment object

    def post(self, request, * args, **kwargs):
        assignment_instance = Assignment.objects.get(id=request.session.get('assignment_id'))
        assignment_instance.name = request.POST.get('assignment_name')
        assignment_instance.desc = request.POST.get('assignment_desc')
        assignment_deadline = request.POST.get('assignment_deadline')
        if assignment_deadline is not '':
            assignment_instance.deadline = timezone.make_aware(datetime.datetime.now() + datetime.timedelta(days=int(assignment_deadline)))
        assignment_instance.save()
        return AssignmentLV.get(request, args, kwargs)

class ProfessorDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'judge/professor/professor_assignment_delete.html'

# Student area------------------------------------------------------------------------------------------------------------------------
class StudentAssignment(LoginRequiredMixin, FormView):
    template_name = 'judge/student/student_assignment.html'
    form_class = CodingForm

    def post(self, request, * args, **kwargs):
        return render(request, self.template_name)

'''
# This page shows result of a assiginment.
class ProfessorResultLV(ListView, LoginManager):
    # We need to revise sub_seq_id
    sub_seq_id = 2
    sql = 'SELECT judge_student.student_id,judge_student.student_name,score \
            FROM judge_student,judge_submit,judge_assignment \
            WHERE judge_assignment.sub_seq_id = judge_submit.sub_seq_id \
            AND judge_student.student_id = judge_submit.student_id \
            AND judge_assignment.sequence = judge_submit.sequence_id \
            AND judge_submit.sub_seq_id = ' + str(sub_seq_id) + ';'

    queryset = Student.objects.raw(sql)
    template_name = 'judge/professor/professor_result_list.html'
    context_object_name = "objects"

class ProfessorCreateView(FormView, LoginManager):
    template_name = 'judge/professor/professor_assignment_add.html'
    form_class = AssignmentForm

#    def form_valid(self, form):
        #return render(self.request, self.template_name, {'form': self.form})
#        return super().form_valid(form)

    def handle_uploaded_file(self, files, path):
        uploaded_file_name = ['in', 'out']
        for f in files:
            with open(path + '/temp/' + uploaded_file_name[files.index(f)], 'wb+') as dest:
                for chunk in f.chunks():
                    dest.write(chunk)

    def post(self, request, *args, **kwargs):
        judgeManager = JudgeManager()
        judgeManager.construct(request.session['professor_id'])
        base_file_path = judgeManager.get_file_path(request.session['subject_id'], request.session['professor_id'])
        self.handle_uploaded_file([request.FILES['in_file'], request.FILES['out_file']], base_file_path)

        #judgeManager.create_problem(request.session['professor_id'], request.session['subject_id'])
        judgeManager.add_assignment(request.session['subject_id'], request.POST.get('assignment_name'),
                request.POST.get('assignment_desc'), int(request.POST.get('deadline')))


        # we need next step which is inserting db.

        return redirect(reverse_lazy('judge:subject', args=[request.session['title'], request.session['classes']]))


#class ProfessorUpdateView(UpdateView):
class ProfessorUpdateView(TemplateView, LoginManager):
    template_name = 'judge/professor/professor_assignment_update.html'

#class ProfessorDeleteView(DeleteView):
class ProfessorDeleteView(TemplateView, LoginManager):
    template_name = 'judge/professor/professor_assignment_delete.html'

#class ProfessorSettingsView(UpdateView):
class ProfessorSettingsView(TemplateView, LoginManager):
    template_name = 'judge/professor/professor_subject_settings.html'

'''
'''
class StudentSubjectLV(TemplateView, LoginManager):
    queryset = None
    template_name = 'judge/student/student_subject_list.html'

    def common(self, request):
        if request.session['subject_id']:
            now = datetime.datetime.now()
            common_sql = ' \
                    SELECT sequence, assignment_name, lf.student_id, deadline, score, max_score \
                    FROM ( \
                    SELECT sequence, assignment_name, judge_student.student_id, deadline, max_score, judge_assignment.sub_seq_id \
                    FROM judge_student \
                    INNER JOIN (judge_signup_class, judge_assignment) \
                    ON (judge_student.student_id = judge_signup_class.student_id \
                    AND judge_signup_class.sub_seq_id = judge_assignment.sub_seq_id) \
                    WHERE judge_assignment.sub_seq_id = {0} \
                    AND judge_student.student_id = "{1}" \
                    AND judge_assignment.sub_seq_id = {0}) as lf \
                    LEFT JOIN judge_submit \
                    ON (lf.sequence = judge_submit.sequence_id \
                    AND lf.student_id = judge_submit.student_id \
                    AND lf.sub_seq_id = judge_submit.sub_seq_id) \
                    WHERE deadline '.format(request.session["subject_id"], request.session['student_id'])

            not_expired_assignment_list_sql = common_sql + '> "{0}";'.format(now)
            expired_assignment_list_sql = common_sql + '< "{0}";'.format(now)

            not_expired_assignment_list = Student.objects.raw(not_expired_assignment_list_sql)
            expired_assignment_list = Student.objects.raw(expired_assignment_list_sql)

            return render(request, self.template_name,
                    { 'not_expired_assignment_list': not_expired_assignment_list,
                      'expired_assignment_list': expired_assignment_list })
        else:
            return HttpResponse('This is wrong way!')


    def get(self, request, *args, **kwargs):
        return self.common(request)

    def post(self, request, *args, **kwargs):
        form = request.POST
        request.session['title'] = form.get('title')
        request.session['classes'] = form.get('classes')
        request.session['subject_id'] = form.get('subject_id')

        return self.common(request)

class StudentAssignment(FormView, LoginManager):
    template_name = 'judge/student/student_assignment.html'
    form_class = CodingForm

    def post(self, request, *args, **kwargs):
        judgeManager = JudgeManager()
        sequence = request.POST.get('sequence')
        
        # into assignment page
        if sequence:
            lang_name = judgeManager.get_lang_name(
                    judgeManager.get_lang_pri_key(request.session['subject_id']))
            assign_info = { 
                'lang': lang_name, 
                'name': judgeManager.get_assign_name(request.session['subject_id'], sequence), 
                'desc': judgeManager.get_assign_desc(request.session['subject_id'], sequence) 
            }
            request.session['sequence'] = sequence
            return render(request, self.template_name, {'assign_info': assign_info, 'form': CodingForm})

        # submit assignment
        else:
            judgeManager = JudgeManager()
            form = CodingForm(request.POST)
            sequence = request.session['sequence']
            del request.session['sequence']

            if form.is_valid():
                code = form.cleaned_data['code']
                code = code.encode('utf-8')
                judgeManager.create_src_file(code, request.session['student_id'], request.session['subject_id'], sequence)
                # we are here
                judgeManager.judge(request.session['subject_id'], request.session['student_id'], sequence)

            return redirect(reverse_lazy('judge:std_subject', args=[request.session['title'], request.session['classes']]))

'''