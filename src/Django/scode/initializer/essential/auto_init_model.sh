#!/bin/bash

rm judge/migrations/000* > /dev/null 2>&1
mysql < initializer/essential/recreate_db

python3 manage.py makemigrations
python3 manage.py migrate

echo "Creating config file..."
python3 initializer/essential/initialize_auto_conf.py
echo "Config file was created!"
