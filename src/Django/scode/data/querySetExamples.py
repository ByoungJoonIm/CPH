from judge.models import *

user_id = 4     #professor 00001

user = User.objects.filter(id=user_id).get()
signup_class = Signup_class.objects.filter(user_id=user_id).values_list('subject_id')
subject = Subject.objects.filter(pk__in = signup_class)

print(user)
print(signup_class)
print(subject)



#for obj in signup_class:    # iteration을 하면 get()을 각각 하는 효과
#    print(obj.id)
