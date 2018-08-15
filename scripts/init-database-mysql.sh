#!/bin/bash

. $(dirname $0)/env.sh

cd "${ROOTDIR}"

DBUSER='escapegame'
DBNAME='escapegame'
DBPASS='escapegame'
DBHOST='localhost'

echo "[client]" > "${HOME}/.my.cnf"

MYSQL_VERSION=$(sudo mysql -s -N -e "select @@version")
VERSION_PREFIX=$(echo $MYSQL_VERSION | tr '.' '\n' | head -n 2 | tr '\n' '.' | sed 's/\.$//')
SUPPORT_IF_EXISTS=$(echo "$VERSION_PREFIX>=5.7" | bc)
IF_EXISTS=''
if [ "$SUPPORT_IF_EXISTS" -eq '1' ]; then
	IF_EXISTS='IF EXISTS '
fi

# Only the MySQL root user can drop or create the database, insert users etc
sudo mysql -u root -e "DROP USER $IF_EXISTS '${DBUSER}'@'${DBHOST}'"
sudo mysql -u root -e "DROP DATABASE IF EXISTS ${DBNAME}"
sudo mysql -u root -e "CREATE DATABASE ${DBNAME} CHARACTER SET utf8"
sudo mysql -u root -e "CREATE USER '${DBUSER}'@'localhost' IDENTIFIED BY '${DBPASS}'"
sudo mysql -u root -e "GRANT ALL PRIVILEGES ON escapegame.* TO '${DBUSER}'@'${DBHOST}'"

# Create MySQL user config
cat <<EOF > ${HOME}/.my.cnf
[client]
database = ${DBNAME}
user = ${DBUSER}
password = ${DBPASS}
default-character-set = utf8
EOF

# Clean all existings migrations to avoid conflicts
rm -f */migrations/0*.py

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
