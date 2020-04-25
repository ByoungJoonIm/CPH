# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# You can see follow address for checking schema
# https://github.com/BJ-Lim/Capstone_Design/blob/master/database/db_schema_v2.PNG
class Language(models.Model):
    lang_id = models.CharField(max_length=10, primary_key=True)
    mode = models.CharField(max_length=10)
    extension = models.CharField(max_length=10)
    template = models.TextField()

class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, db_column = 'language_id')
    hided = models.BooleanField(default=False)

class Signup_class_base(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, db_column = 'subject_id')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Signup_class_student(Signup_class_base):
    accepted = models.BooleanField(default = False)

class Signup_class_professor(Signup_class_base):
    owner = models.BooleanField(default = False)

class Assignment(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    desc = models.TextField()
    deadline = models.DateTimeField(null=False)
    max_score = models.IntegerField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, db_column = 'subject_id')
    problem = models.BinaryField()

    #It will work like setter
    def problem_upload(self, file_src_path):
        file_binary = open(file_src_path, "rb")
        self.problem = file_binary.read()
        file_binary.close()

    #It will work like getter
    def problem_download(self, file_dest_path):
        dest = open(file_dest_path, "wb")
        dest.write(self.problem)
        dest.close()

class Submit(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=100, null=True)
    score = models.IntegerField()
    submit_time = models.DateTimeField()
    code = models.TextField()
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
