#!/bin/bash

rm ../judge/migrations/000* > /dev/null 2>&1
mysql < recreate_db

python3 ../manage.py makemigrations
python3 ../manage.py migrate
#python3 ../manage.py migrate judge
#mysql < sqlchecker
