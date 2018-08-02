#!/bin/bash

if ! [ -f db.sqlite3 ]; then
	./scripts/init-database.sh
fi

python3 manage.py runserver
