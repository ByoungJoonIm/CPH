# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# You can see follow address for checking schema
# https://github.com/BJ-Lim/Capstone_Design/blob/master/database/db_schema_v2.PNG

class Language(models.Model):
    pri_key = models.AutoField(primary_key = True)
    name = models.CharField(max_length=10)
    extention = models.CharField(max_length=10)
    lang_id = models.CharField(max_length=10)

#class subject(models.Model, common):
class Subject(models.Model):
    pri_key = models.AutoField(primary_key=True)
    year = models.CharField(max_length=4, null=False)
    semester = models.IntegerField(null=False)
    subject_cd = models.CharField(max_length=20, null=False)
    classes = models.CharField(max_length=2, null=False)

    title = models.CharField(max_length=100)
    grade = models.IntegerField()

    lang_seq = models.ForeignKey(Language, on_delete=models.CASCADE)

    # we need to make it remove redundancy
    input_id = models.CharField(max_length=45)
    input_ip = models.CharField(max_length=45)
    input_date = models.DateTimeField(auto_now_add=True, null=True)
    update_id = models.CharField(max_length=45)
    update_ip = models.CharField(max_length=45)
    update_date = models.DateTimeField(auto_now=True, null=True)
    class Meta:
        unique_together = ('year', 'semester', 'subject_cd', 'classes')


class Student(models.Model):
    student_id = models.CharField(max_length=10, primary_key=True)
    student_name = models.CharField(max_length=45)
    password = models.CharField(max_length=64)

    # we need to make it remove redundancy
    input_id = models.CharField(max_length=45)
    input_ip = models.CharField(max_length=45)
    input_date = models.DateTimeField(auto_now_add=True)
    update_id = models.CharField(max_length=45)
    update_ip = models.CharField(max_length=45)
    update_date = models.DateTimeField(auto_now=True)


class Professor(models.Model):
    professor_id = models.CharField(max_length=10, primary_key=True)
    professor_name = models.CharField(max_length=45)
    password = models.CharField(max_length=64)

    # we need to make it remove redundancy
    input_id = models.CharField(max_length=45)
    input_ip = models.CharField(max_length=45)
    input_date = models.DateTimeField(auto_now_add=True)
    update_id = models.CharField(max_length=45)
    update_ip = models.CharField(max_length=45)
    update_date = models.DateTimeField(auto_now=True)

class Signup_class(models.Model):
    # Table must have one key in Django
    not_use_pri_key = models.AutoField(primary_key=True)
    # sub_seq same as year, semester, subject_cd, classes
    sub_seq = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    # we need to make it remove redundancy
    input_id = models.CharField(max_length=45)
    input_ip = models.CharField(max_length=45)
    input_date = models.DateTimeField(auto_now_add=True)
    update_id = models.CharField(max_length=45)
    update_ip = models.CharField(max_length=45)
    update_date = models.DateTimeField(auto_now=True)

class Subject_has_professor(models.Model):
    # Table must have one key in Django
    not_use_pri_key = models.AutoField(primary_key=True)
    # sub_seq same as year, semester, subject_cd, classes
    sub_seq = models.ForeignKey(Subject, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    represent_yn = models.BooleanField(default=False)
    # we need to add a field that has size of assignment here.

    # we need to make it remove redundancy
    input_id = models.CharField(max_length=45)
    input_ip = models.CharField(max_length=45)
    input_date = models.DateTimeField(auto_now_add=True)
    update_id = models.CharField(max_length=45)
    update_ip = models.CharField(max_length=45)
    update_date = models.DateTimeField(auto_now=True)


class Assignment(models.Model):
    not_use_pri_key = models.AutoField(primary_key=True)
    sequence = models.IntegerField(null=False)
    # sub_seq same as year, semester, subject_cd, classes
    sub_seq = models.ForeignKey(Subject, on_delete=models.CASCADE)
    assignment_name = models.CharField(max_length=100)
    assignment_desc = models.TextField()
    deadline = models.DateTimeField(null=False)
    max_score = models.IntegerField()
	
    # we need to make it remove redundancy
    input_id = models.CharField(max_length=45)
    input_ip = models.CharField(max_length=45)
    input_date = models.DateTimeField(auto_now_add=True)
    update_id = models.CharField(max_length=45)
    update_ip = models.CharField(max_length=45)
    update_date = models.DateTimeField(auto_now=True)

class Submit(models.Model):
    # Table must have one key in Django
    not_use_pri_key = models.AutoField(primary_key=True)
    sequence = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    sub_seq = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100, null=True)
    score = models.IntegerField()


