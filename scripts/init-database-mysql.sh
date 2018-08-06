#!/bin/bash

. $(dirname $0)/env.sh

cd "${ROOTDIR}"

DBUSER='escapegame'
DBNAME='escapegame'
DBPASS='escapegame'
DBHOST='localhost'

echo "[client]" > "${HOME}/.my.cnf"

# Only the MySQL root user can drop or create the database, insert users etc
sudo mysql -u root -e "
	DROP DATABASE IF EXISTS ${DBNAME};
	DROP USER IF EXISTS '${DBUSER}'@'${DBHOST}';
	CREATE DATABASE ${DBNAME} CHARACTER SET utf8;
	CREATE USER '${DBUSER}'@'localhost' IDENTIFIED BY '${DBPASS}';
	GRANT ALL PRIVILEGES ON escapegame.* TO '${DBUSER}'@'${DBHOST}';"

# Create MySQL user config
cat <<EOF > ${HOME}/.my.cnf
[client]
database = ${DBNAME}
user = ${DBUSER}
password = ${DBPASS}
default-character-set = utf8
EOF

# Create database
${PYTHON} manage.py makemigrations
${PYTHON} manage.py migrate

# Create superuser
LOGIN='gamemaster'
MAIL='none@mail.com'
PASS='pbkdf2_sha256$100000$jdNRfA8s4xZc$QS9LDv1ntYYWSO445RL1aVeTFWwLcU2cLMLyuy1G0Lc='
DATE=$(date +"%Y-%m-%d %H:%M:%S.%6N")
mysql -u ${DBUSER} -e "
	INSERT INTO auth_user VALUES(1,'${PASS}',NULL,1,'${LOGIN}','','','${MAIL}',1,1,'${DATE}');" ${DBNAME}

# Populate database
${PYTHON} manage.py shell < ./scripts/populate-database.py
