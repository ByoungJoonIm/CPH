#------add users
def add_users():
    from django.contrib.auth.models import User, Group
    
    student_group = Group.objects.get(name="student")
    professor_group = Group.objects.get(name="professor")

    for i in range(20160001, 20160004):
        user = User.objects.create_user(username = str(i), password = str(i))
        student_group.user_set.add(user)

    for i in range(1, 3):
        user = User.objects.create_user(username = "0000" + str(i), password = "0000" + str(i))
        professor_group.user_set.add(user)
        
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
        ['C_Sample','C'],
        ['Python_Sample','PY3'],
        ['Java_Sample','JAVA8'],
    ]
    
    for r in relation:
        title = r[0]
        lang_id = r[1]
        
        subject = Subject.objects.create(
            title=title,
            language=Language.objects.get(lang_id=lang_id)
        )
    
add_subject()

#------add signup_class
def add_signup_class():
    from judge.models import Subject, Signup_class
    from django.contrib.auth.models import User

    relation = [
        [1, 1],
        [2, 1],
        [3, 1],
        [1, 4],
        [2, 4],
        [3, 4]
    ]
    
    for r in relation:
        subject = Subject.objects.get(id=r[0])
        user = User.objects.get(id=r[1])
        
        signup_class = Signup_class.objects.create(
            subject = subject,
            user = user
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
    
    problem_bin_code = b'PK\x03\x04\x14\x00\x00\x00\x00\x00\xe8\x90\x93P\x94\xe8\x16w\x04\x00\x00\x00\x04\x00\x00\x00\x04\x00\x00\x001.in1 1\nPK\x03\x04\x14\x00\x00\x00\x00\x00\xe8\x90\x93P\x90\xaf|L\x02\x00\x00\x00\x02\x00\x00\x00\x05\x00\x00\x001.out2\nPK\x03\x04\x14\x00\x00\x00\x00\x00\xe8\x90\x93Pa\x1a:\xb0\x05\x00\x00\x00\x05\x00\x00\x00\x04\x00\x00\x002.in-1 0\nPK\x03\x04\x14\x00\x00\x00\x00\x00\xe8\x90\x93P\r\xe2\\\xe9\x03\x00\x00\x00\x03\x00\x00\x00\x05\x00\x00\x002.out-1\nPK\x01\x02\x14\x03\x14\x00\x00\x00\x00\x00\xe8\x90\x93P\x94\xe8\x16w\x04\x00\x00\x00\x04\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa4\x81\x00\x00\x00\x001.inPK\x01\x02\x14\x03\x14\x00\x00\x00\x00\x00\xe8\x90\x93P\x90\xaf|L\x02\x00\x00\x00\x02\x00\x00\x00\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa4\x81&\x00\x00\x001.outPK\x01\x02\x14\x03\x14\x00\x00\x00\x00\x00\xe8\x90\x93Pa\x1a:\xb0\x05\x00\x00\x00\x05\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa4\x81K\x00\x00\x002.inPK\x01\x02\x14\x03\x14\x00\x00\x00\x00\x00\xe8\x90\x93P\r\xe2\\\xe9\x03\x00\x00\x00\x03\x00\x00\x00\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa4\x81r\x00\x00\x002.outPK\x05\x06\x00\x00\x00\x00\x04\x00\x04\x00\xca\x00\x00\x00\x98\x00\x00\x00\x00\x00'
    
    for r in relations:
        assignment = Assignment.objects.create(
            name = r[0],
            desc = 'Input a, b\nOutput a + b',
            deadline = timezone.make_aware(datetime.datetime.now() + datetime.timedelta(days=r[2])),
            max_score = 2,
            subject = Subject.objects.get(id=r[1]),
            problem = problem_bin_code
        )

        
add_assignment()