#!/bin/bash

epath=initializer/essential

rm judge/migrations/000* > /dev/null 2>&1
mysql < $epath/recreate_db

python3 manage.py makemigrations
python3 manage.py migrate

# This block will uncomment when project is done.
#echo "Creating config file..."
#python3 $epath/initialize_auto_conf.py
#echo "Config file was created!"

rm -r ~/assignment_cache > /dev/null 2>&1
python3 $epath/create_directories.py
