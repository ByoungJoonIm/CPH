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
        
    language = Language.objects.create(
        lang_id = 'PY3',
        mode = 'python',
        extension = 'py',
        template = '#python template is not supported yet\n')
    language.save()
    
    language = Language.objects.create(
        lang_id = 'C',
        mode = 'c_cpp',
        extension = 'c',
        template = '#include <stdio.h>\n\nvoid main(){\n\t\n}')
    language.save()
    
    language = Language.objects.create(
        lang_id = 'JAVA8',
        mode = 'java',
        extension = 'java',
        template = 'import java.util.*;\n\npublic class Main{\n\tpublic static void main(String args[]){\n\t\t\n\t}\n}')
    language.save()
    
add_languages()

#------add next samples