#!/bin/bash

#for i in "student" "professor" "subject" "assignment" "signup_class" "subject_has_professor" "submit";do
for i in "language" "subject" "signup_class" "assignment" ;do

python3 manage.py loaddata test/$i.yaml
done

rm -r ~/judge_files 2> /dev/null
