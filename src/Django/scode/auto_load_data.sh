#!/bin/bash

rm -r ~/student_codes
./test/./auto_init_model.sh
python3 manage.py shell < data/adder.py
./test/./auto_loaddata.sh

