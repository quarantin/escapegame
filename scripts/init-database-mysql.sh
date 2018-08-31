#!/bin/bash -x

. $(dirname $0)/env.sh

cd "${ROOTDIR}"

DBNAME=escapegame
DBUSER=escapegame
DBPASS=escapegame
DBPORT=3306

CREATE_MYSQL_CLIENT_CONFIG(){

	DBHOST=$1

	# Create MySQL user config
	cat <<EOF > ${HOME}/.my.cnf
[client]
host = ${DBHOST}
port = ${DBPORT}
database = ${DBNAME}
user = ${DBUSER}
password = ${DBPASS}
default-character-set = utf8
EOF
}

CREATE_MYSQL_ROOT_CONFIG(){

	# Reset mysql client configuration
	echo "[client]" > "${HOME}/.my.cnf"

	DBHOST=localhost
}

CREATE_MYSQL_DATABASE(){

	sudo mysql -u root -e "DROP DATABASE IF EXISTS ${DBNAME}"
	sudo mysql -u root -e "CREATE DATABASE ${DBNAME} CHARACTER SET utf8"
}

CREATE_MYSQL_USER(){

	DB_HOST=$1

	MYSQL_VERSION=$(sudo mysql -s -N -e "select @@version")
	VERSION_PREFIX=$(echo $MYSQL_VERSION | tr '.' '\n' | head -n 2 | tr '\n' '.' | sed 's/\.$//')
	SUPPORT_IF_EXISTS=$(echo "$VERSION_PREFIX>=5.7" | bc)
	IF_EXISTS=''
	if [ "$SUPPORT_IF_EXISTS" -eq '1' ]; then
		IF_EXISTS='IF EXISTS '
	fi

	sudo mysql -u root -e "DROP USER $IF_EXISTS '${DBUSER}'@'${DB_HOST}'"
	sudo mysql -u root -e "CREATE USER '${DBUSER}'@'${DB_HOST}' IDENTIFIED BY '${DBPASS}'"
	sudo mysql -u root -e "GRANT ALL PRIVILEGES ON escapegame.* TO '${DBUSER}'@'${DB_HOST}'"
}

CREATE_DJANGO_USER(){

	# Create superuser
	LOGIN='gamemaster'
	MAIL='none@mail.com'
	PASS='pbkdf2_sha256$100000$jdNRfA8s4xZc$QS9LDv1ntYYWSO445RL1aVeTFWwLcU2cLMLyuy1G0Lc='
	DATE=$(date +"%Y-%m-%d %H:%M:%S.%6N")
	sudo mysql -u root -e "INSERT INTO auth_user VALUES(1,'${PASS}',NULL,1,'${LOGIN}','','','${MAIL}',1,1,'${DATE}')" "${DBNAME}"
}

MASTER(){

	CREATE_MYSQL_ROOT_CONFIG

	CREATE_MYSQL_DATABASE

	CREATE_MYSQL_USER localhost

	# Create database
	${PYTHON} manage.py makemigrations
	${PYTHON} manage.py migrate

	# Populate database
	${PYTHON} manage.py populate-database

	CREATE_DJANGO_USER

	RASPIS=$(${PYTHON} manage.py shell < "${ROOTDIR}/scripts/show-remote-controllers.py")
	for RASPI in $RASPIS; do
		CREATE_MYSQL_USER $RASPI
	done

	MYSQL_SERVER=localhost
}

SLAVE(){

	MYSQL_SERVER="${MASTER_HOSTNAME}"
}

if [ $HOSTNAME == $MASTER_HOSTNAME ]; then
	MASTER
else
	SLAVE
fi

CREATE_MYSQL_CLIENT_CONFIG "${MYSQL_SERVER}"
