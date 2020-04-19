from django import forms
from django_ace import AceWidget

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
    code = forms.CharField(widget=AceWidget(mode='javascript', theme='twilight'), label='code')
    
    def __init__(self, *args, **kwargs):
        mode = kwargs.pop('mode')
        template = kwargs.pop('template')
        super().__init__(*args, **kwargs)
        self.fields['code'].widget.mode = mode
        self.fields['code'].initial = template
        
        print(len(template))
        print(len('#include <stdio.h>\n\nint main(int argc, char *argv[]){\n\t\n}'))
            