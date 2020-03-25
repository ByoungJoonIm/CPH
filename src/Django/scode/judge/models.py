# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# You can see follow address for checking schema
# https://github.com/BJ-Lim/Capstone_Design/blob/master/database/db_schema_v2.PNG

class Language(models.Model):
    lang_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=10)
    extension = models.CharField(max_length=10)

class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    year = models.CharField(max_length=4, null=False)
    semester = models.IntegerField(null=False)
    subject_cd = models.CharField(max_length=20, null=False)
    classes = models.CharField(max_length=2, null=False)
    title = models.CharField(max_length=100)
    grade = models.IntegerField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE, db_column = 'language_id')

    class Meta:
        unique_together = ('year', 'semester', 'subject_cd', 'classes')

class Signup_class(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, db_column = 'subject_id')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Assignment(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    desc = models.TextField()
    deadline = models.DateTimeField(null=False)
    max_score = models.IntegerField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, db_column = 'subject_id')

class Submit(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=100, null=True)
    score = models.IntegerField()
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, db_column = 'assignment_id')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, db_column = 'subject_id')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column = 'user_id')
