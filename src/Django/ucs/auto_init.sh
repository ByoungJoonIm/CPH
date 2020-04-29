#!/bin/bash

epath=initializer/essential/
spath=initializer/sample/

echo "Initailizing model..."
./$epath./auto_init_model.sh
echo "Initailizing model was completed!"

echo "Inserting sample datas..."
python3 manage.py shell < $epath/group_adder.py
python3 manage.py shell < $spath/sample_adder.py
echo "Inserting sample datas was completed!"

