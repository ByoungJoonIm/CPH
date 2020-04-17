#!/bin/bash

for i in "language" "subject" "signup_class" "assignment" ;do
python3 manage.py loaddata initializer/sample/$i.yaml
done
