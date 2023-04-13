#!/bin/bash

cd rhixescans && source env/bin/activate &&
#python3 manage.py dumpdata --natural-foreign --natural-primary -e contenttypes --indent 4 > db.json ; 
python3 manage.py dumpdata --natural-foreign --natural-primary --indent 4 > db.json ; 
python3 manage.py flush && 
python3 manage.py loaddata db.json