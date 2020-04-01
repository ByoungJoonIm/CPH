from django import forms

class AssignmentForm(forms.Form):
    assignment_name = forms.CharField(label="assignment_name")
    assignment_desc = forms.CharField(label="assignment_desc", widget=forms.Textarea)
    assignment_deadline = forms.IntegerField(label="assignment_deadline", initial=7)
    assignment_in_file = forms.FileField(label="assignment_in_file")
    assignment_out_file = forms.FileField(label="assignment_out_file")

class CodingForm(forms.Form):
    code = forms.CharField(widget=forms.Textarea(), label="code")
