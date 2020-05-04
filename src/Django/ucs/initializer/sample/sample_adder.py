#------add users
def add_users():    
    from judge.models import Professor, Student
    from django.contrib.auth.models import Permission
    
    student_permission = Permission.objects.get(codename='student')
    professor_permission = Permission.objects.get(codename='professor')
    
    for i in range(20160001, 20160010):
        student = Student.objects.create_user(username = str(i), password = str(i))
        student.user_permissions.add(student_permission)

    for i in range(1, 9):
        professor = Professor.objects.create_user(username = "0000" + str(i), password = "0000" + str(i))
        professor.user_permissions.add(professor_permission)
       
add_users()


#------add languages
def add_languages():
    from judge.models import Language
    
    relation = [
        ['PY3', 'python', 'py', '#python template is not supported yet\n'],
        ['C', 'c_cpp', 'c', '#include <stdio.h>\n\nvoid main(){\n\t\n}'],
        ['JAVA8', 'java', 'java', 'import java.util.*;\n\npublic class Main{\n\tpublic static void main(String args[]){\n\t\t\n\t}\n}']
    ]
    
    for r in relation:
        Language.objects.create(
            lang_id = r[0],
            mode = r[1],
            extension = r[2],
            template = r[3]
        )
        
    
add_languages()

#------add Subject
def add_subject():
    from judge.models import Language, Subject
    
    relation = [
        ['C_Sample','C', 'access01'],
        ['Python_Sample','PY3', 'access02'],
        ['Java_Sample','JAVA8', 'access03'],
    ]
    
    for r in relation:
        title = r[0]
        lang_id = r[1]
        access_code = r[2]
        
        subject = Subject.objects.create(
            title=title,
            language=Language.objects.get(lang_id=lang_id),
            access_code = access_code
        )
    
add_subject()

#------add signup_class
def add_signup_class():
    from judge.models import Subject, Signup_class_student, Signup_class_professor
    from django.contrib.auth.models import User

    relation_student = [
        [1, 1, 1],
        [2, 1, 1],
        [3, 1, 1],
        [1, 2, 1],
        [2, 2, 1],
        [3, 2, 1],
        [1, 3, 1],
        [2, 3, 1],
        [3, 3, 1],
    ]
    
    relation_professor = [
        [1, 10, 4],
        [2, 10, 4],
        [3, 10, 4]
    ]
    
    for r in relation_student:
        subject = Subject.objects.get(id=r[0])
        user = User.objects.get(id=r[1])
        state = r[2]
        
        Signup_class_student.objects.create(
            subject = subject,
            user = user,
            state = state
        )
        
    for r in relation_professor:
        subject = Subject.objects.get(id=r[0])
        user = User.objects.get(id=r[1])
        state = r[2]
        
        Signup_class_professor.objects.create(
            subject = subject,
            user = user,
            state = state
        ) 
        
add_signup_class()

#------add assignment
def add_assignment():
    from judge.models import Subject, Assignment
    import os
    from django.utils import timezone
    import datetime
    
    relations = [
        ['c_aplusb', 1, 7],
        ['python_aplusb', 2, 7],
        ['java_aplusb', 3, 7],
        ['c_aplusb_expired', 1, -7],
        ['python_aplusb_expired', 2, -7],
        ['java_aplusb_expired', 3, -7]
    ]
    
    sample_path = os.getcwd()
    sample_path = os.path.join(sample_path, "initializer")
    sample_path = os.path.join(sample_path, "sample")
    sample_path = os.path.join(sample_path, "problem.zip")
    problem_bin_code = None
    
    with open(sample_path, "rb") as p:
         problem_bin_code = p.read()
    
    for r in relations:
        assignment = Assignment.objects.create(
            name = r[0],
            desc = 'Input a, b\nOutput a + b',
            deadline = timezone.make_aware(datetime.datetime.now() + datetime.timedelta(days=r[2])),
            max_score = 3,
            subject = Subject.objects.get(id=r[1]),
            problem = problem_bin_code
        )

        
add_assignment()
