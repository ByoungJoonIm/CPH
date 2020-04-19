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

from django.contrib import messages

from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin

from judge.models import *
from judge.forms import AssignmentForm, AssignmentUpdateForm, CodingForm, SubjectForm


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
from ansi2html import Ansi2HTMLConverter

from bs4 import BeautifulSoup

#-- Here is developing area    
# common area------------------------------------------------------------------------------------------------------------------------
class UserMainLV(LoginRequiredMixin, ListView):
    template_name = 'judge/common/common_subject_list.html'
    
    @classmethod
    def get(self, request, *args, **kwargs):
        signup_class = Signup_class.objects.filter(user_id=request.user.id).values_list('subject_id')
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
class ProfessorAddSubjectView(LoginRequiredMixin, FormView):
    template_name = 'judge/professor/professor_subject_add.html'
    form_class = SubjectForm
    
    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        lang_id = request.POST.get('language')
        
        subject_instance = Subject.objects.create(
            title = title,
            language = Language.objects.get(lang_id=lang_id)
        )
        
        signup_class_instance = Signup_class.objects.create(
            subject = subject_instance,
            user = request.user
        )
        
        return UserMainLV.get(request)
    
class ProfessorAddView(LoginRequiredMixin, FormView):
    template_name = 'judge/professor/professor_assignment_add.html'
    form_class = AssignmentForm

    def post(self, request, *args, **kwargs):
        self.generate_assignment(self.request)
            
        return AssignmentLV.get(request, args, kwargs)  

    def generate_assignment(self, request):
        #--- Creating assignment directory 
        temp_path = os.path.join(os.path.join(os.path.expanduser('~'), 'assignment_cache'), request.user.username + "_temp")
        os.mkdir(temp_path)
        
        origin_path = os.getcwd()
        os.chdir(temp_path)
        
        #--- upload files
        origin_file_name = ['assignment_in_file', 'assignment_out_file']
        uploaded_file_name = ['in', 'out']
            
        for seq in range(0, 2):
            with open(uploaded_file_name[seq], 'wb+') as dest:
                for chunk in request.FILES[origin_file_name[seq]].chunks():
                    dest.write(chunk)                    
                    
        #--- separate files
        in_file = open("in", "r")
        out_file = open("out", "r")
        cnt = 0

        zip_name = "problem.zip"
        myzip = zipfile.ZipFile(zip_name, "w")

        file_list = ["in", "out", "problem.zip"]

        while True:
            in_line = in_file.readline().rstrip()
            out_line = out_file.readline().rstrip()
            if not in_line or not out_line:
                break

            cnt = cnt + 1
            
            in_file_rs_name = str(cnt) + ".in"
            in_file_rs = open(in_file_rs_name, "w")
            in_file_rs.write(str(in_line) + '\n')
            in_file_rs.close()

            out_file_rs_name = str(cnt) + ".out"
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

        #--- insert to database
        assignment_instance = Assignment()    
        assignment_instance.name = request.POST.get('assignment_name')
        assignment_instance.desc = request.POST.get('assignment_desc')
        assignment_instance.deadline = timezone.make_aware(datetime.datetime.now() + datetime.timedelta(days=int(request.POST.get('assignment_deadline'))))
        assignment_instance.max_score = cnt
        assignment_instance.subject = Subject.objects.get(id=int(request.session.get('subject_id')))
        assignment_instance.problem_upload(zip_name)
        assignment_instance.save()

        #--- remove files
        for f in file_list:
            os.remove(f)
        os.chdir(origin_path)
        os.rmdir(temp_path)
        
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
    form_class = CodingForm(mode='c_cpp', template='#It is not general way')
    #we need to change mode by language in get or post(maybe get)
    #Is form_class variable necessary?
    
    def get(self, request, * args, **kwargs):
        assignment_id = request.GET.get('assignment_id')
        
        if not assignment_id:
            assignment_id = request.session.get('assignment_id')
        else:
           request.session['assignment_id'] = assignment_id
        
        assignment = Assignment.objects.get(id=assignment_id)
        language = Language.objects.get(lang_id=Subject.objects.get(id=request.session.get('subject_id')).language_id)
        coding_form = CodingForm(mode=language.mode, template=language.template)
        
        # If get page with wrong answer
        if 'judge_result' in kwargs.keys():
            judge_result = kwargs.pop('judge_result')
            return render(request, self.template_name,
                       {'form' : CodingForm(mode=language.mode, template=judge_result['last_code']),
                         'assignment' : assignment,
                         'lang' : language,
                         'result' : judge_result['result']})
        
        # basic get
        return render(request, self.template_name,
                       {'form' : coding_form,
                         'assignment' : assignment,
                         'lang' : language})

    def post(self, request, * args, **kwargs):
        code = request.POST.get('code')
        
        # time_weight has to be deleted. Now, docker container doesn't have correct time.
        time_weight = datetime.timedelta(hours=9)
        submit_time = timezone.make_aware(datetime.datetime.now() + time_weight)
        
        assignment = Assignment.objects.get(id=request.session.get('assignment_id'))
        language = Language.objects.get(lang_id=Subject.objects.get(id=request.session.get('subject_id')).language_id)
        base_dir_path = os.path.join(os.path.join(os.path.expanduser('~'), 'assignment_cache'), str(assignment.id))
        
        # This code will be changed to do something
        if submit_time > assignment.deadline:
            print("Deadline is alreay expired!")
        else:
            print("This submit_itme is valid!")
        
        # here, we need to clone file that is needed from db
        
        if not os.path.exists(base_dir_path):
            self.create_structure(base_dir_path, assignment)
        
        self.create_src_file(code, os.path.join(base_dir_path, "students"),assignment, language, request)
        
        context = dict()
        judge_result = self.judge_student_src_file(submit_time, code, base_dir_path, assignment, language, request, context)
        
        if judge_result:
            return AssignmentLV.get(request)
        
        context['judge_result'] = judge_result
        context['last_code'] = code
        
        return self.get(request, judge_result=context)
        
    def create_structure(self, base_dir_path, assignment):
        origin_path = os.getcwd()
        
        os.mkdir(base_dir_path)
        os.chdir(base_dir_path)
        
        for dirs in ["problem", "students"]:
            os.mkdir(dirs)
        
        #--- generate init and problem.zip file
        init_file = open(os.path.join("problem", "init.yml"), "w")
        init_file.write("archive: problem.zip\ntest_cases:")

        for i in range(1, assignment.max_score + 1):
            init_file.write("\n- {" + "in: {0}.in, out: {0}.out, points: 1".format(i) + "}")

        init_file.close()
        assignment.problem_download(os.path.join("problem", "problem.zip"))
        
        #--- generate config file
        config_file = open("config.yml", "w")
        base_config_file = open(os.path.join(os.path.join(os.path.expanduser('~'), "settings"), "base_config.yml"), "r")
        
        config_file.write("problem_storage_root:\n  -  {0}\n".format(base_dir_path))

        while True:
            line = base_config_file.readline()
            if not line:
                break
            config_file.write(line)
            
        config_file.close()
        base_config_file.close()
        
        os.chdir(origin_path)

    
    def create_src_file(self, code, student_dir_path, assignment, language, request):        
        src_path = os.path.join(student_dir_path, request.user.username + "." + language.extension)
        
        src_file = open(src_path, "w")
        src_file.write(code)
        src_file.close()
        
    def judge_student_src_file(self, submit_time, code, base_dir_path, assignment, language, request, context):
        config_file_path = os.path.join(base_dir_path, "config.yml")
        init_file_path = os.path.join(os.path.join(base_dir_path, "problem"), "init.yml")
        
        student_file_path = os.path.join(base_dir_path, "students")
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

        max_score = sum(points)
        # Make parsed result of dmoj-judge
        a = subprocess.check_output(["dmoj-cli", "-c", config_file_path, "-e", language.lang_id, "submit", "problem", language.lang_id, student_file_path ])
        sp = [s.decode("utf-8") for s in a.split()] #convert byte to string

        i = 0
        total_get = 0
        result_output = "\n".join(a.decode("utf-8").split("\n")[6:-3])
        result_html = Ansi2HTMLConverter().convert(result_output)
        bs = BeautifulSoup(result_html,'html.parser')
        context['result'] = str(bs.find('pre'))
        
        ac_ansi = '\x1b[1m\x1b[32mAC\x1b[0m'
        
        while True:
            if sp[i] == "Done":
                break
            if sp[i] == "Test":
                if sp[i+3] == ac_ansi:
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
            if submit_instance.score <= total_get:
                submit_instance.code = code
                submit_instance.submit_time = submit_time
            submit_instance.save()
            
        return total_get == max_score
