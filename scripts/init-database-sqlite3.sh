#!/bin/bash

. $(dirname $0)/env.sh

cd "${ROOTDIR}"

# Clear database, migrations, etc.
./clean.sh

# Create database
${PYTHON} manage.py makemigrations
${PYTHON} manage.py migrate

# Create superuser
LOGIN='gamemaster'
MAIL='none@mail.com'
PASS='pbkdf2_sha256$100000$jdNRfA8s4xZc$QS9LDv1ntYYWSO445RL1aVeTFWwLcU2cLMLyuy1G0Lc='
DATE=$(date +"%Y-%m-%d %H:%M:%S.%6N")
sqlite3 ./db.sqlite3 "INSERT INTO 'auth_user' VALUES(1,'${PASS}',NULL,1,'${LOGIN}','','${MAIL}',1,1,'${DATE}','');"

# Populate database
${PYTHON} manage.py shell < scripts/populate-database.py
