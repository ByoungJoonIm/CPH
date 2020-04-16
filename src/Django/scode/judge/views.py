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
import subprocess
import yaml
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
        self.generate_config_file(base_dir_path)
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
    
    def create_base_autoconf(self):
        base_config_path = os.path.expanduser('~')
        base_config_path = os.path.join(base_config_path, 'settings')
        base_config_path = os.path.join(base_config_path, 'base_config.yml')
        
        cmd = "dmoj-autoconf 1>" + base_config_path + " 2>/dev/null" 
        subprocess.call(cmd, shell=True)
    
    def generate_config_file(self, base_dir_path):
        base_config_path = os.path.join(os.path.join(os.path.expanduser('~'), "settings"), "base_config.yml")
        if not os.path.exists(base_config_path):
            self.create_base_autoconf()
            
        config_path = os.path.join(base_dir_path, "settings")
        config_path = os.path.join(config_path, "config.yml")
        
        config_file = open(config_path, "w")
        base_config_file = open(base_config_path, "r")
        
        config_file.write("problem_storage_root:\n  -  " + os.path.join(base_dir_path, 'problems') + "\n")

        while True:
            line = base_config_file.readline()
            if not line:
                break
            config_file.write(line)
            
        config_file.close()
        base_config_file.close()
    
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

        for i in range(1, cnt + 1):
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
        assignment_instance.sequence = sequence
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
    
    def get(self, request, * args, **kwargs):
        assignment_id = request.GET.get('assignment_id')
        request.session['assignment_id'] = assignment_id
        
        return render(request, self.template_name,
                       {'form' : self.form_class,
                         'assignment' : Assignment.objects.get(id=assignment_id),
                         'lang' : Language.objects.get(lang_id=Subject.objects.get(id=request.session.get('subject_id')).language_id)})   # + current assignment object

    def post(self, request, * args, **kwargs):
        coding_form = CodingForm(request.POST)
        code = request.POST.get('code')
        
        base_dir_path = self.get_base_dir_path(request)
        assignment = Assignment.objects.get(id=request.session.get('assignment_id'))
        language = Language.objects.get(lang_id=Subject.objects.get(id=request.session.get('subject_id')).language_id)
        
        self.create_src_file(code, os.path.join(base_dir_path, "students"),assignment, language, request)
        self.judge_student_src_file(base_dir_path, assignment, language, request)
        
        return render(request, self.template_name)
    
    def get_base_dir_path(self, request):
        subject = Subject.objects.get(id=request.session.get('subject_id'))
        professor_id = Signup_class.objects.filter(subject_id=subject.id)
        professor_number = User.objects.filter(groups__name="professor").filter(pk__in=professor_id.values_list('user_id')).values('username')[0]['username']
        
        #/user/student_codes/2019_1/00001/Algorithm_01/temp
        base_dir_path = os.path.expanduser('~')
        base_dir_path = os.path.join(base_dir_path, "student_codes")
        base_dir_path = os.path.join(base_dir_path, str(subject.year) + "_" + str(subject.semester))
        base_dir_path = os.path.join(base_dir_path, professor_number)
        base_dir_path = os.path.join(base_dir_path, subject.title + "_" + subject.classes)
        return base_dir_path
    
    def create_src_file(self, code, student_dir_path, assignment, language, request):        
        src_path = os.path.join(student_dir_path, str(assignment.sequence))
        src_path = os.path.join(src_path, request.user.username + "." + language.extension)
        
        src_file = open(src_path, "w")
        src_file.write(code)
        src_file.close()
        
    def judge_student_src_file(self, base_dir_path, assignment, language, request):
        sequence = str(assignment.sequence)
        
        config_file_path = os.path.join(base_dir_path, "settings")
        config_file_path = os.path.join(config_file_path, "config.yml")
        
        init_file_path = os.path.join(base_dir_path, "problems")
        init_file_path = os.path.join(init_file_path, sequence)
        init_file_path = os.path.join(init_file_path, "init.yml")
        
        student_file_path = os.path.join(base_dir_path, "students")
        student_file_path = os.path.join(student_file_path, sequence)
        student_file_path = os.path.join(student_file_path, request.user.username + "." + language.extension)
        
        
        points = []
        with open(init_file_path, 'r') as stream:
            try:
                prob_info = yaml.safe_load(stream)
                tc = prob_info['test_cases']
                for t in tc:
                    points.append(t['points'])
            except yaml.YAMLError as exc:
                print(exc)

        # Make parsed result of dmoj-judge
        a = subprocess.check_output(["dmoj-cli", "-c", config_file_path, "--no-ansi", "-e", language.lang_id, "submit", sequence, language.lang_id, student_file_path ])
        sp = a.split()

        i = 0
        total_get = 0

        while True:
            if i >= len(sp):
                break
            if sp[i] == "Done":
                break
            if sp[i].decode("utf-8") == "Test":
                if str(sp[i+3].decode("utf-8")) == "AC":
                    total_get = total_get + points[int(sp[i + 2]) - 1]

            i = i + 1

        # update score in submit table in database
        submit_instance = None
        try:
            submit_instance = Submit.objects.filter(assignment_id = assignment.id).get(user_id=request.user.id)
            submit_instance.score = max(submit_instance.score, total_get)
        except Submit.DoesNotExist:
            submit_instance = Submit(assignment = assignment, user=request.user, score = total_get)
        finally:
            submit_instance.save()
            
            
            
