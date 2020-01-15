#!/bin/bash

cd test
./auto_init_model.sh
cd ..
python3 manage.py shell < data/adder.py
