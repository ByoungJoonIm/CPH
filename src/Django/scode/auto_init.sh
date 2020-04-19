#!/bin/bash

epath=initializer/essential/
spath=initializer/sample/

./$epath./auto_init_model.sh
python3 manage.py shell < $epath/group_adder.py

python3 manage.py shell < $spath/sample_adder.py
./$spath./auto_add_sample_data.sh

