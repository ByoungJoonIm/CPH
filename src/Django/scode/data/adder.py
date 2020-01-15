from django.contrib.auth.models import User, Group

#----------------------group setting
student_group = Group.objects.create(name="student")
professor_group = Group.objects.create(name="professor")

#----------------------initial user setting
for i in range(20160001, 20160004):
    user = User.objects.create_user(str(i), str(i))
    student_group.user_set.add(user)
    user.save()

for i in range(1, 3):
    user = User.objects.create_user("0000" + str(i), "0000" + str(i))
    professor_group.user_set.add(user)
    user.save()
