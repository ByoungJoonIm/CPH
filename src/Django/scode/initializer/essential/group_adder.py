def init_groups():
    from django.contrib.auth.models import User, Group
    
    student_group = Group.objects.create(name="student")
    professor_group = Group.objects.create(name="professor")

init_groups()

