#!/bin/bash

rm -f db.sqlite

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser --user gamemater --email none@mail.com
