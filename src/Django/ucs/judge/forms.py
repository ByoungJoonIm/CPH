from django import forms
from django_ace import AceWidget
from judge.choices import *


class SubjectForm(forms.Form):
    title = forms.CharField(label="title", widget=forms.TextInput(), required=True)
    language = forms.ChoiceField(choices = LANGUAGE_CHOICES, label="language", widget=forms.Select(), required=True)   

class StudentSubjectAddForm(forms.Form):
    subject_id = forms.IntegerField(label="subject_id", required=True)
    access_code = forms.CharField(label="access_code", required=True)
    
class AssignmentForm(forms.Form):
    assignment_name = forms.CharField(label="assignment_name")
    assignment_desc = forms.CharField(label="assignment_desc", widget=forms.Textarea)
    assignment_deadline = forms.IntegerField(label="assignment_deadline", initial=7)
    assignment_in_file = forms.FileField(label="assignment_in_file")
    assignment_out_file = forms.FileField(label="assignment_out_file")

class AssignmentUpdateForm(AssignmentForm):
    assignment_deadline = forms.IntegerField(label="assignment_deadline", required=False)
    assignment_in_file = forms.FileField(label="assignment_in_file", required=False)
    assignment_out_file = forms.FileField(label="assignment_out_file", required=False)

class CodingForm(forms.Form):
    code = forms.CharField(widget=AceWidget(mode='javascript', theme='twilight', width="1000px", height="400px"), label='code')
    
    def __init__(self, *args, **kwargs):
        mode = kwargs.pop('mode')
        template = kwargs.pop('template')
        super().__init__(*args, **kwargs)
        self.fields['code'].widget.mode = mode
        self.fields['code'].initial = template