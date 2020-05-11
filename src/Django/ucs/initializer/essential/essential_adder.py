#------add groups(Actually, this is not used at this time)
def add_groups():
    from django.contrib.auth.models import User, Group
    
    student_group = Group.objects.create(name="student")
    professor_group = Group.objects.create(name="professor")

add_groups()



#------add languages
def add_languages():
    from judge.models import Language
    
    relation = [
        ['PY3', 'python', 'py', '#python template is not supported yet\n'],
        ['C', 'c_cpp', 'c', '#include <stdio.h>\n\nint main(){\n\t\n\treturn 0;\n}'],
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